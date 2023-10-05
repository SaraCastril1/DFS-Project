# Importar las bibliotecas necesarias
from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Función para convertir la cadena de texto en una función evaluable
def parse_function(expr):
    x = sp.symbols('x')
    return sp.lambdify(x, expr, 'numpy')

def bisection(f, a, b, tol, max_iterations):
    f = parse_function(f)  # Convertir la expresión en una función evaluable
    if f(a) * f(b) >= 0:
        raise ValueError('La función no cumple con el teorema del valor intermedio en el intervalo dado.')

    print('Iteración\t  a\t\t  b\t\t  c\t\t  f(c)\t\t  Error')

    for iteration in range(1, max_iterations + 1):
        c = (a + b) / 2
        fc = f(c)

        # Calcular el error en esta iteración
        e = abs(b - a)

        print(f'{iteration:4d}\t\t{a:8.6f}\t{b:8.6f}\t{c:8.6f}\t{fc:8.6f}\t{e:8.6f}')

        if abs(fc) < tol:
            print(f'La solución aproximada es c = {c:8.6f} después de {iteration} iteraciones.')
            return c

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    print(f'El método de bisección no convergió después de {max_iterations} iteraciones.')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None  # Inicializa el resultado como None

    if request.method == 'POST':
        function_text = request.form['function']
        a = float(request.form['a'])
        b = float(request.form['b'])
        tol = float(request.form['Tolerance']) 
        max_iterations = int(request.form['Nitter'])  
        
        # Llama a la función de bisección aquí con los valores ingresados
        try:
            result = bisection(function_text, a, b, tol, max_iterations)
        except ValueError as e:
            result = str(e)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
