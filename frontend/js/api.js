export const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Универсальная функция для выполнения fetch-запросов
 */
export async function request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
        }

        // Если ответ пустой (например, 204 No Content), возвращаем null
        if (response.status === 204) return null;

        return await response.json();
    } catch (error) {
        console.error(`API Request failed: ${endpoint}`, error);
        throw error;
    }
}