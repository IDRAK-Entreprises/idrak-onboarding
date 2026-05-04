<script setup>
import { onMounted, ref } from 'vue'

const API_URL = 'http://localhost:8000'

const nextOrder = ref(null)
const completedOrders = ref([])
const workerStats = ref(null)
const workerId = ref(1)
const message = ref('')
const loading = ref(false)

async function loadQueue() {
  try {
    const response = await fetch(`${API_URL}/orders/queue`)

    if (!response.ok) {
      nextOrder.value = null
      return
    }

    nextOrder.value = await response.json()
  } catch {
    nextOrder.value = null
  }
}

async function loadCompletedOrders() {
  const response = await fetch(`${API_URL}/orders?status=completed`)
  completedOrders.value = await response.json()
}

async function loadWorkerStats() {
  const response = await fetch(`${API_URL}/workers/${workerId.value}/stats`)

  if (response.ok) {
    workerStats.value = await response.json()
  }
}

async function refreshData() {
  await loadQueue()
  await loadCompletedOrders()
  await loadWorkerStats()
}

async function fulfillOrder() {
  if (!nextOrder.value) {
    return
  }

  loading.value = true
  message.value = ''

  const response = await fetch(`${API_URL}/orders/${nextOrder.value.id}/fulfill`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      worker_id: Number(workerId.value)
    })
  })

  if (response.ok) {
    message.value = `Order #${nextOrder.value.id} completed`
    await refreshData()
  } else {
    const error = await response.json()
    message.value = error.detail || 'Something went wrong'
  }

  loading.value = false
}

onMounted(refreshData)
</script>

<template>
  <main class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">IDRAK Warehouse Dashboard</p>
        <h1>Order Packing Queue</h1>
        <p class="subtitle">
          View the next order in the queue, assign a worker, and mark it as fulfilled.
        </p>
      </div>

      <button class="refresh" @click="refreshData">
        Refresh
      </button>
    </section>

    <section class="grid">
      <div class="card main-card">
        <div class="card-header">
          <div>
            <p class="label">Next Order</p>
            <h2 v-if="nextOrder">Order #{{ nextOrder.id }}</h2>
            <h2 v-else>No orders waiting</h2>
          </div>

          <span v-if="nextOrder" class="status">
            {{ nextOrder.status }}
          </span>
        </div>

        <div v-if="nextOrder" class="order-content">
          <div class="meta">
            <div>
              <span>Created</span>
              <strong>{{ new Date(nextOrder.created_at).toLocaleString() }}</strong>
            </div>

            <div>
              <span>Items</span>
              <strong>{{ nextOrder.items.length }}</strong>
            </div>
          </div>

          <div class="items">
            <div v-for="item in nextOrder.items" :key="item.id" class="item">
              <div>
                <strong>{{ item.product_name }}</strong>
                <p>{{ item.bottle_style_name }}</p>
              </div>
              <span>x{{ item.quantity }}</span>
            </div>
          </div>

          <div class="fulfill-box">
            <label>
              Worker ID
              <input v-model="workerId" type="number" min="1" />
            </label>

            <button :disabled="loading" @click="fulfillOrder">
              {{ loading ? 'Fulfilling...' : 'Fulfill Order' }}
            </button>
          </div>

          <p v-if="message" class="message">{{ message }}</p>
        </div>

        <div v-else class="empty">
          <p>The queue is empty. Create an order from the API docs to test the dashboard.</p>
        </div>
      </div>

      <div class="side">
        <div class="card">
          <p class="label">Worker Stats</p>
          <h2 v-if="workerStats">{{ workerStats.worker_name }}</h2>
          <h2 v-else>Worker</h2>

          <p class="big-number">
            {{ workerStats ? workerStats.total_orders_fulfilled : 0 }}
          </p>
          <p class="muted">orders fulfilled</p>
        </div>

        <div class="card">
          <p class="label">Completed Orders</p>

          <div v-if="completedOrders.length" class="completed-list">
            <div v-for="order in completedOrders" :key="order.id" class="completed">
              <span>Order #{{ order.id }}</span>
              <strong>{{ order.items.length }} items</strong>
            </div>
          </div>

          <p v-else class="muted">No completed orders yet.</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 40px;
  background:
    radial-gradient(circle at top left, rgba(71, 118, 230, 0.25), transparent 35%),
    linear-gradient(135deg, #0f172a, #111827);
  color: #e5e7eb;
  font-family: Inter, system-ui, sans-serif;
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.eyebrow,
.label {
  color: #38bdf8;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.75rem;
  font-weight: 700;
}

h1 {
  font-size: 3rem;
  margin: 8px 0;
}

h2 {
  margin: 4px 0 0;
  font-size: 1.7rem;
}

.subtitle {
  color: #94a3b8;
  max-width: 560px;
}

.refresh,
button {
  border: 0;
  border-radius: 14px;
  padding: 12px 18px;
  background: #38bdf8;
  color: #082f49;
  font-weight: 800;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.grid {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr;
  gap: 24px;
}

.card {
  background: rgba(15, 23, 42, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 28px;
  padding: 28px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(18px);
}

.main-card {
  min-height: 520px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
}

.status {
  background: rgba(34, 197, 94, 0.16);
  color: #86efac;
  padding: 8px 12px;
  border-radius: 999px;
  text-transform: capitalize;
  font-weight: 700;
}

.meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin: 28px 0;
}

.meta div {
  background: rgba(30, 41, 59, 0.9);
  padding: 18px;
  border-radius: 18px;
}

.meta span,
.muted,
.item p {
  color: #94a3b8;
}

.meta strong {
  display: block;
  margin-top: 6px;
}

.items {
  display: grid;
  gap: 12px;
}

.item,
.completed {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(30, 41, 59, 0.75);
  padding: 16px;
  border-radius: 18px;
}

.item p {
  margin: 4px 0 0;
}

.item span {
  font-size: 1.25rem;
  font-weight: 800;
  color: #38bdf8;
}

.fulfill-box {
  margin-top: 28px;
  display: flex;
  gap: 12px;
  align-items: end;
}

label {
  display: grid;
  gap: 8px;
  color: #cbd5e1;
  font-weight: 700;
}

input {
  width: 120px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  border-radius: 12px;
  padding: 12px;
  background: #020617;
  color: #e5e7eb;
}

.message {
  margin-top: 18px;
  color: #86efac;
  font-weight: 700;
}

.empty {
  margin-top: 100px;
  color: #94a3b8;
  text-align: center;
}

.side {
  display: grid;
  gap: 24px;
}

.big-number {
  font-size: 4rem;
  font-weight: 900;
  margin: 20px 0 0;
  color: #38bdf8;
}

.completed-list {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}

@media (max-width: 900px) {
  .page {
    padding: 22px;
  }

  .hero {
    display: grid;
    gap: 20px;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 2.2rem;
  }

  .fulfill-box {
    flex-direction: column;
    align-items: stretch;
  }

  input {
    width: 100%;
  }
}
</style>
