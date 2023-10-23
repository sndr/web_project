document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const message = document.getElementById("message");

    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const username = document.getElementById("usuario").value;
        const password = document.getElementById("senha").value;

        // Implemente sua lógica de validação aqui
        if (validateLogin(username, password)) {
            message.textContent = "Login bem-sucedido!";
        } else {
            message.textContent = "Credenciais inválidas. Tente novamente.";
        }
    });

    function validateLogin(username, password) {
        // Simulação de validação (substitua com sua lógica real)
        if (username === "bh" && password === "1233") {
            return true;
        }
        return false;
    }
});
