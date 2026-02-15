// Get the task list, task input, submit button, and filters from the DOM
let taskList = document.getElementById('task-list');
let taskInput = document.getElementById('task-input');
let submitButton = document.getElementById('submit-button');
let filters = document.querySelectorAll('.filter');

// Define the addTask function to add a new task to the list
function addTask(task) {
    // Create a new task element
    let taskElement = document.createElement('li');
    taskElement.textContent = task;
    taskElement.classList.add('task');
    
    // Add the task to the list
    taskList.appendChild(taskElement);
}

// Define the deleteTask function to delete a task from the list
function deleteTask(task) {
    // Get the task element
    let taskElement = taskList.querySelector(`.task[textContent='${task}']`);
    
    // Remove the task from the list
    if (taskElement) {
        taskList.removeChild(taskElement);
    }
}

// Define the completeTask function to mark a task as completed
function completeTask(task) {
    // Get the task element
    let taskElement = taskList.querySelector(`.task[textContent='${task}']`);
    
    // Mark the task as completed
    if (taskElement) {
        taskElement.classList.add('completed');
    }
}

// Define the filterTasks function to filter tasks by status
function filterTasks(status) {
    // Get all tasks
    let tasks = taskList.children;
    
    // Filter tasks based on the status
    for (let task of tasks) {
        if (status === 'all') {
            task.style.display = 'block';
        } else if (status === 'active' && task.classList.contains('completed')) {
            task.style.display = 'none';
        } else if (status === 'completed' && !task.classList.contains('completed')) {
            task.style.display = 'none';
        }
    }
}
