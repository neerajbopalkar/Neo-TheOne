/**
 * Display Handler - Responsible for UI state and DOM updates
 * Separation of Concerns: Handles only display-related operations
 */
class Display {
    constructor(elementId = 'display') {
        this.element = document.getElementById(elementId);
        this.value = '0';
    }

    setValue(value) {
        this.value = value;
        this.element.value = value;
    }

    getValue() {
        return this.value;
    }

    append(content) {
        if (this.value === '0' && content !== '.') {
            this.setValue(content);
        } else {
            this.setValue(this.value + content);
        }
    }

    clear() {
        this.setValue('0');
    }

    deleteLastChar() {
        const newValue = this.value.length > 1 ? this.value.slice(0, -1) : '0';
        this.setValue(newValue);
    }

    showError() {
        this.setValue('Error');
    }

    reset() {
        this.setValue('0');
    }
}

/**
 * Input Validator - Validates user input
 * Single Responsibility: Only validates, doesn't execute
 */
class InputValidator {
    static isNumber(value) {
        return value >= '0' && value <= '9';
    }

    static isOperator(value) {
        return ['+', '-', '*', '/'].includes(value);
    }

    static isDecimalPoint(value) {
        return value === '.';
    }

    static hasDecimalPoint(expression) {
        return expression.includes('.');
    }

    static endsWithOperator(expression) {
        return this.isOperator(expression[expression.length - 1]);
    }

    static isValidExpression(expression) {
        if (expression === '' || expression === '0') return false;
        if (this.endsWithOperator(expression)) return false;
        return true;
    }
}

/**
 * Calculator Engine - Business logic for calculations
 * Single Responsibility: Only handles calculation logic
 * Dependency Inversion: Depends on abstraction (Display), not concrete implementation
 */
class CalculatorEngine {
    constructor(display) {
        this.display = display;
    }

    appendNumber(num) {
        if (InputValidator.isDecimalPoint(num)) {
            if (!InputValidator.hasDecimalPoint(this.display.getValue())) {
                this.display.append(num);
            }
        } else {
            this.display.append(num);
        }
    }

    appendOperator(operator) {
        const currentValue = this.display.getValue();
        const lastChar = currentValue[currentValue.length - 1];

        if (InputValidator.isOperator(lastChar)) {
            // Replace the last operator
            this.display.setValue(currentValue.slice(0, -1) + operator);
        } else if (currentValue === '') {
            this.display.setValue('0' + operator);
        } else {
            this.display.append(operator);
        }
    }

    calculate() {
        const expression = this.display.getValue();

        if (!InputValidator.isValidExpression(expression)) {
            return;
        }

        try {
            const result = this.evaluateExpression(expression);
            this.display.setValue(result);
        } catch (error) {
            this.display.showError();
            setTimeout(() => this.display.reset(), 1500);
        }
    }

    evaluateExpression(expression) {
        // Use Function constructor instead of eval for safer evaluation
        const safeEval = new Function('return ' + expression);
        let result = safeEval();

        // Handle floating point precision
        result = Math.round(result * 100000000) / 100000000;

        return result;
    }

    clear() {
        this.display.clear();
    }

    deleteLastChar() {
        this.display.deleteLastChar();
    }
}

/**
 * Input Handler - Manages keyboard and mouse input
 * Single Responsibility: Maps input to calculator actions
 * Dependency Inversion: Depends on CalculatorEngine abstraction
 */
class InputHandler {
    constructor(calculator) {
        this.calculator = calculator;
        this.setupKeyboardListeners();
    }

    setupKeyboardListeners() {
        document.addEventListener('keydown', (event) => {
            this.handleKeyboardInput(event);
        });
    }

    handleKeyboardInput(event) {
        const key = event.key;

        if (InputValidator.isNumber(key)) {
            this.calculator.appendNumber(key);
        } else if (InputValidator.isDecimalPoint(key)) {
            this.calculator.appendNumber(key);
        } else if (InputValidator.isOperator(key)) {
            event.preventDefault();
            this.calculator.appendOperator(key);
        } else if (key === 'Enter' || key === '=') {
            event.preventDefault();
            this.calculator.calculate();
        } else if (key === 'Backspace') {
            event.preventDefault();
            this.calculator.deleteLastChar();
        } else if (key === 'Escape') {
            this.calculator.clear();
        }
    }
}

/**
 * Application Initializer
 * Orchestrates component creation and dependency injection
 */
class CalculatorApp {
    constructor() {
        this.display = new Display('display');
        this.calculator = new CalculatorEngine(this.display);
        this.inputHandler = new InputHandler(this.calculator);
        this.setupUIClickHandlers();
    }

    setupUIClickHandlers() {
        // Map button click handlers
        const handlers = {
            'C': () => this.calculator.clear(),
            'DEL': () => this.calculator.deleteLastChar(),
            '=': () => this.calculator.calculate(),
        };

        // Attach click handlers to buttons
        document.querySelectorAll('.btn').forEach((button) => {
            button.addEventListener('click', () => {
                const text = button.innerText;

                if (handlers[text]) {
                    handlers[text]();
                } else if (InputValidator.isOperator(text)) {
                    this.calculator.appendOperator(text.replace('÷', '/').replace('×', '*').replace('−', '-'));
                } else if (InputValidator.isNumber(text) || InputValidator.isDecimalPoint(text)) {
                    this.calculator.appendNumber(text);
                }
            });
        });
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new CalculatorApp();
});
