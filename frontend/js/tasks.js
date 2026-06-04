import { request } from './api.js';
import { getUserNameById } from './users.js';

let tasks = [];
let currentTaskId = null;
let taskDetailsModal = null;

// Инициализация модального окна (вызывается из main.js)
export function initTaskModal(modalInstance) {
    taskDetailsModal = modalInstance;
}

export async function loadTasks(statusFilter = '') {
    const tbody = document.getElementById('tasksTableBody');
    tbody.innerHTML = '<tr><td colspan="7" class="text-center py-4"><div class="spinner-border text-primary" role="status"></div></td></tr>';

    try {
        const endpoint = statusFilter ? `/tasks?status=${statusFilter}` : '/tasks';
        tasks = await request(endpoint);
        renderTasks(tasks);
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger py-4">Ошибка загрузки данных: ' + error.message + '</td></tr>';
    }
}

export async function createTask(payload) {
    try {
        await request('/tasks', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        return true;
    } catch (error) {
        alert('Ошибка создания задачи: ' + error.message);
        return false;
    }
}

export async function updateTask(id, payload) {
    try {
        await request(`/tasks/${id}`, {
            method: 'PUT',
            body: JSON.stringify(payload)
        });
        return true;
    } catch (error) {
        alert('Ошибка обновления задачи: ' + error.message);
        return false;
    }
}

export async function deleteTask(id) {
    if (!confirm('Вы уверены, что хотите удалить эту задачу? Это действие необратимо.')) {
        return false;
    }

    try {
        await request(`/tasks/${id}`, {
            method: 'DELETE'
        });
        return true;
    } catch (error) {
        alert('Ошибка удаления задачи: ' + error.message);
        return false;
    }
}

export function renderTasks(tasksData) {
    const tbody = document.getElementById('tasksTableBody');
    const emptyState = document.getElementById('emptyState');
    tbody.innerHTML = '';

    if (tasksData.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    emptyState.style.display = 'none';

    const statusLabels = {
        'new': '<span class="badge status-new">Новая</span>',
        'in_progress': '<span class="badge status-in_progress">В работе</span>',
        'done': '<span class="badge status-done">Выполнена</span>',
        'cancelled': '<span class="badge status-cancelled">Отменена</span>'
    };

    tasksData.forEach(task => {
        const tr = document.createElement('tr');
        tr.className = 'task-card';

        const assigneeName = task.assignee_name || getUserNameById(task.assignee_id) || '<span class="text-muted">Не назначен</span>';
        const updatedDate = new Date(task.updated_at).toLocaleString('ru-RU', {
            day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit'
        });

        tr.innerHTML = `
            <td>#${task.id}</td>
            <td class="fw-bold">${escapeHtml(task.title)}</td>
            <td>${escapeHtml(task.requester)}</td>
            <td>${assigneeName}</td>
            <td>${statusLabels[task.status] || task.status}</td>
            <td class="text-muted small">${updatedDate}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-primary edit-task-btn" data-id="${task.id}">
                    <i class="bi bi-pencil-square"></i> Изменить
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

export function openTaskDetails(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    currentTaskId = task.id;
    document.getElementById('updateTaskId').value = task.id;
    document.getElementById('modalTaskTitle').textContent = `Задача #${task.id}: ${task.title}`;
    document.getElementById('modalTaskDescription').textContent = task.description;
    document.getElementById('modalTaskRequester').textContent = task.requester;

    document.getElementById('updateStatus').value = task.status;
    document.getElementById('updateAssignee').value = task.assignee_id || '';

    taskDetailsModal.show();
}

export function getCurrentTaskId() {
    return currentTaskId;
}

export function resetCurrentTaskId() {
    currentTaskId = null;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}