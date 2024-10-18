# The Shamir's Secret Sharing (SSS) scheme as well as the mathematical concepts involved.

![5vvByhKF1sdG1BLuFfwSCR](https://github.com/user-attachments/assets/b63dc29c-ea6b-4186-ba29-2794d8501877)

### Code Breakdown with Mathematical Explanation:

The primary purpose of this code is to implement **Shamir's Secret Sharing** (SSS), which is a method for splitting a secret into multiple parts, or **shares**, such that the secret can only be reconstructed if a threshold number of shares are combined. If fewer than the required number of shares are available, the secret remains secure.

#### 1. **Shamir's Secret Sharing Overview**
Shamir's Secret Sharing is based on polynomial interpolation, specifically **Lagrange interpolation**. The idea is to encode the secret as the constant term of a polynomial. Each share is a point on this polynomial, and a minimum number of shares (`threshold`) are needed to reconstruct the secret using the polynomial's interpolation.

The mathematical foundation here is that you can define a unique polynomial of degree `t-1` (where `t` is the threshold number of shares) using `t` points. The constant term of this polynomial is the secret.

#### 2. **Step-by-Step Breakdown**

##### **Password Generation (`PasswordGenerator` class)**
This class generates a random password (used here as the secret). It chooses random digits from `string.digits` to create a password of a given length.

```python
class PasswordGenerator:
    @staticmethod
    def generate_random_password(length=10):
        password = "".join(random.choices(string.digits, k=length))
        return password
```
- **Random Password**: This will generate a numeric string (e.g., "1234567890"), which is converted into an integer and treated as the secret for the scheme.

##### **Generating the Polynomial and Shares (`SecretSharing` class)**

This class manages the core functions of Shamir's Secret Sharing, such as generating the polynomial and shares, and reconstructing the secret.

1. **Generate Coefficients for the Polynomial:**
   
   ```python
   def generate_coefficients(self, secret):
       coefficients = [random.randrange(0, FIELD_SIZE) for _ in range(self.threshold - 1)]
       coefficients.append(secret)  # Add the secret as the constant term
       return coefficients
   ```
   - **Explanation**: This function generates the coefficients for a polynomial of degree `threshold - 1` (i.e., a polynomial with `threshold` terms).
   - The constant term of this polynomial is the secret itself. For example, if `threshold = 3`, the polynomial might look like:
     \[
     f(x) = ax^2 + bx + \text{secret}
     \]
   where `a` and `b` are random coefficients, and the constant term is the secret.

2. **Generate Shares:**
   
   ```python
   def generate_shares(self, secret):
       coefficients = self.generate_coefficients(secret)
       shares = [(x, self.polynom(x, coefficients)) for x in random.sample(range(1, FIELD_SIZE), self.num_shares)]
       return shares
   ```
   - **Explanation**: This function generates `num_shares` points (shares) from the polynomial.
     - For each `x`, it calculates a corresponding `y` value using the polynomial formula (`polynom` method).
     - Each `(x, y)` pair forms a share. The `x` values are randomly chosen from the range `1` to `FIELD_SIZE`.

   **Mathematical Context**:
   - The function evaluates the polynomial at different `x` values to produce the points (shares). For example, for a polynomial:
     \[
     f(x) = ax^2 + bx + \text{secret}
     \]
     When `x = 1`, the share might be `(1, f(1))`; when `x = 2`, the share might be `(2, f(2))`, and so on.
   
   Each share represents a point on this polynomial curve.

3. **Evaluate Polynomial at a Given `x`:**

   ```python
   def polynom(self, x, coefficients):
       point = sum(coefficient * (x ** index) for index, coefficient in enumerate(coefficients))
       return point
   ```
   - **Explanation**: This method calculates the value of the polynomial at a given `x` using the list of coefficients.
     - For example, if the polynomial is \( f(x) = ax^2 + bx + \text{secret} \), then when `x=2`, it calculates:
       \[
       f(2) = a \cdot 2^2 + b \cdot 2 + \text{secret}
       \]
     - The result is the `y` value of the share corresponding to that `x`.

##### **Reconstructing the Secret:**
The secret is reconstructed using **Lagrange interpolation**. This allows you to reconstruct the polynomial from a set of points (shares) and recover the constant term (the secret).

1. **Reconstruct the Secret (`reconstruct_secret` method):**

   ```python
   def reconstruct_secret(self, shares):
       total = Decimal(0)

       for j, (xj, yj) in enumerate(shares):
           prod = Decimal(1)

           for i, (xi, _) in enumerate(shares):
               if i != j:
                   prod *= Decimal(xi) / (xi - xj)

           total += prod * yj

       secret = int(round(total))
       return secret
   ```
   - **Explanation**: This function reconstructs the secret from the shares using **Lagrange interpolation**.
     - **Lagrange Interpolation** allows us to reconstruct a polynomial from a set of points. The polynomial's constant term is the secret.
     - The formula for Lagrange interpolation is:
       \[
       f(0) = \sum_{j=0}^{t-1} y_j \prod_{i=0, i \neq j}^{t-1} \frac{x_i}{x_i - x_j}
       \]
     - In this code:
       - `xj`, `yj` are the x and y coordinates of the j-th share.
       - The inner loop calculates the product term \( \prod_{i=0, i \neq j}^{t-1} \frac{x_i}{x_i - x_j} \), which is part of the Lagrange interpolation formula.
     - The final result is the constant term of the polynomial, which is the secret.

##### **Complete Flow in `main` Function:**

1. A random password (numeric string) is generated and converted into an integer, treated as the secret.
2. The secret is split into shares using Shamir’s Secret Sharing (with `t=3`, `n=5`, meaning 5 shares are created and any 3 can reconstruct the secret).
3. A random subset of the shares (threshold) is chosen, and the secret is reconstructed using those shares.

### Mathematical Flow Summary:
1. **Password (Secret)**: Treated as a constant term of a polynomial.
2. **Polynomial Creation**: Randomly generated coefficients with the secret as the constant term.
3. **Shares**: Points on the polynomial (x, f(x)).
4. **Reconstruction**: Using Lagrange interpolation to reconstruct the polynomial and extract the constant term (secret) from a subset of shares.

#### Example:
- Let’s say the secret is `1234`, and the polynomial generated is:
  \[
  f(x) = 5x^2 + 7x + 1234
  \]
- The generated shares (points on the polynomial) might be:
  - (1, f(1)) = (1, 1246)
  - (2, f(2)) = (2, 1262)
  - (3, f(3)) = (3, 1282)
  - (4, f(4)) = (4, 1306)
  - (5, f(5)) = (5, 1334)
  
- With any 3 of these shares, you can reconstruct the polynomial and recover the constant term (secret `1234`).
