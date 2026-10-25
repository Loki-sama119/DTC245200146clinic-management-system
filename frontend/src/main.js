import { navigate } from './routes/router.js';

window.addEventListener('hashchange', navigate);
window.addEventListener('DOMContentLoaded', navigate);
