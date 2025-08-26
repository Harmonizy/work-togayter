import Alpine from 'alpinejs';
import './styles/main.css';

function counterData() {
    return {
        count: 1,
        increment() {
            this.count+=5;
        },
        decrement() {
            this.count--;
        },
        double() {
            this.count = this.count * 2;
        },
        halfCount() {
            this.count = Math.floor(this.count / 2);
        },
        triplePlusOne() {
            this.count = this.count * 3 + 1;
        }
    };
}

Alpine.data('counterData', counterData);
window.Alpine = Alpine;
Alpine.start(); 