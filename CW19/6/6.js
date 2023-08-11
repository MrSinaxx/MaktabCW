localStorage.setItem('firstName', 'sina');
localStorage.setItem('lastName', 'leylaz');
localStorage.setItem('age', '30');
localStorage.setItem('country', 'iran');
localStorage.setItem('city', 'New York');

const firstName = localStorage.getItem('firstName');
const lastName = localStorage.getItem('lastName');
const age = localStorage.getItem('age');
const country = localStorage.getItem('country');
const city = localStorage.getItem('city');

console.log(firstName, lastName, age, country, city);
