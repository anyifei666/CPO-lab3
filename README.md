# GROUP-"I like studying" - lab 3 - variant 2

This is my lab3 of CPO class,
implementation of mathematical expression by string substitution(Variant2).

## Project structure

- `interpreter.py` -- implementation of the mathematical expression interpreter.
- `test_interpreter.py` -- tests for `interpreter.py`.

## Features

- Evaluate expression: `eval_expr(expr, variables={}, user_functions={})`
- Validate input: `validate_input(expr, variables={}, user_functions={})`
- Visualize expression tree: `visualize_expr(expr, variables={}, user_functions={})`
- Custom functions: Add user-defined functions via `user_functions` parameter.

## Contribution

- AnYifei (645192770@qq.com) -- all work.

## Changelog

- 10.6.2024 - 1
   - Add Visualization.
- 8.6.2024 - 0
   - Initialization.
   - Implementation of all features.
   - Update README.
   - Add tests.

## Design notes

- The interpreter is designed to parse and evaluate mathematical expressions
  given as strings.
- It supports basic arithmetic, built-in mathematical functions, and user-defined
  functions.
- Error handling and input validation ensure robust and secure execution.
- Logging is implemented for transparency during expression evaluation.
