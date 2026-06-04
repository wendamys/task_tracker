import { loadUsers } from './users.js';
import {
    initTaskModal,
    loadTasks,
    createTask,
    updateTask,
    deleteTask,
    openTaskDetails,
    getCurrentTaskId,
    resetCurrentTaskId
} from './tasks.js';

document.addEventListener('DOMContentLoaded', () => {
    // Инициализация Bootstrap модального окна
    const modalElement = document.getElementById('taskDetailsModal');
    const taskDetailsModal = new bootstrap.Modal(modalElement);
    initTaskModal(taskDetailsModal);

    // Начальная загрузка данных
    loadUsers();
    loadTasks();

    // --- Обработчики событий ---

    // 1. Создание задачи
    document.getElementById('createTaskForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('createBtn');
        const spinner = document.getElementById('createSpinner');

        btn.disabled = true;
        spinner.style.display = 'inline-block';

        const assigneeId = document.getElementById('createAssignee').value;
        const payload = {
            title: document.getElementById('createTitle').value,
            description: document.getElementById('createDescription').value,
            requester: document.getElementById('createRequester').value,
            assignee_id: assigneeId ? parseInt(assigneeId) : null
        };

        const success = await createTask(payload);

        if (success) {
            e.target.reset();
            loadTasks(document.getElementById('statusFilter').value);
        }

        btn.disabled = false;
        spinner.style.display = 'none';
    });

    // 2. Фильтрация задач
    document.getElementById('statusFilter').addEventListener('change', (e) => {
        loadTasks(e.target.value);
    });

    // 3. Делегирование события клика на кнопку "Изменить" в таблице
    document.getElementById('tasksTableBody').addEventListener('click', (e) => {
        const editBtn = e.target.closest('.edit-task-btn');
        if (editBtn) {
            const taskId = parseInt(editBtn.dataset.id);
            openTaskDetails(taskId);
        }
    });

    // 4. Сохранение изменений в модальном окне
    document.getElementById('saveTaskBtn').addEventListener('click', async () => {
        const id = getCurrentTaskId();
        if (!id) return;

        const btn = document.getElementById('saveTaskBtn');
        const spinner = document.getElementById('saveSpinner');

        btn.disabled = true;
        spinner.style.display = 'inline-block';

        const assigneeId = document.getElementById('updateAssignee').value;
        const payload = {
            status: document.getElementById('updateStatus').value,
            assignee_id: assigneeId ? parseInt(assigneeId) : null
        };

        const success = await updateTask(id, payload);

        if (success) {
            taskDetailsModal.hide();
            loadTasks(document.getElementById('statusFilter').value);
        }

        btn.disabled = false;
        spinner.style.display = 'none';
    });

    // 5. Удаление задачи из модального окна
    document.getElementById('deleteTaskBtn').addEventListener('click', async () => {
        const id = getCurrentTaskId();
        if (!id) return;

        const success = await deleteTask(id);

        if (success) {
            taskDetailsModal.hide();
            resetCurrentTaskId();
            loadTasks(document.getElementById('statusFilter').value);
        }
    });

    // 6. Сброс ID при закрытии модального окна (чтобы не было багов при повторном открытии)
    modalElement.addEventListener('hidden.bs.modal', () => {
        resetCurrentTaskId();
    });
});