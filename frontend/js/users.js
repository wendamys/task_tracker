import { request } from './api.js';

let users = [];

export async function loadUsers() {
    try {
        users = await request('/users');
        populateUserSelects();
    } catch (error) {
        alert('Не удалось загрузить список пользователей: ' + error.message);
    }
}

export function populateUserSelects() {
    const createSelect = document.getElementById('createAssignee');
    const updateSelect = document.getElementById('updateAssignee');

    // Сохраняем первую опцию "Не назначен"
    createSelect.innerHTML = '<option value="">Не назначен</option>';
    updateSelect.innerHTML = '<option value="">Не назначен</option>';

    users.forEach(user => {
        const option1 = new Option(user.name, user.id);
        const option2 = new Option(user.name, user.id);
        createSelect.add(option1);
        updateSelect.add(option2);
    });
}

export function getUserNameById(id) {
    const user = users.find(u => u.id === id);
    return user ? user.name : null;
}