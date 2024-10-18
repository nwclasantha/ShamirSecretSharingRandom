#!/usr/bin/env python3
import random
import string
import logging
from decimal import Decimal

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('secret_sharing_class.log'),
        logging.StreamHandler()
    ]
)

FIELD_SIZE = 10**5  # Define the field size used for random number generation


class SecretSharing:
    def __init__(self, threshold, num_shares):
        self.threshold = threshold
        self.num_shares = num_shares

    def reconstruct_secret(self, shares):
        """
        Combines individual shares (points on a graph)
        using Lagrange interpolation to reconstruct the secret.

        `shares` is a list of points (x, y) on a polynomial curve
        where the constant term is the secret.
        """
        try:
            total = Decimal(0)

            for j, (xj, yj) in enumerate(shares):
                prod = Decimal(1)

                for i, (xi, _) in enumerate(shares):
                    if i != j:
                        prod *= Decimal(xi) / (xi - xj)

                total += prod * yj

            secret = int(round(total))
            logging.info(f'Secret successfully reconstructed: {secret}')
            return secret
        except Exception as e:
            logging.error(f"Error reconstructing the secret: {e}")
            raise

    def polynom(self, x, coefficients):
        """
        Generates a single point on the polynomial curve for the given x-value.
        
        `coefficients` is a list where each element is the coefficient of the polynomial.
        """
        try:
            point = sum(coefficient * (x ** index) for index, coefficient in enumerate(coefficients))
            return point
        except Exception as e:
            logging.error(f"Error calculating polynomial point: {e}")
            raise

    def generate_coefficients(self, secret):
        """
        Randomly generates the coefficients for a polynomial of degree `threshold-1`.
        The constant term is the `secret`.
        """
        try:
            coefficients = [random.randrange(0, FIELD_SIZE) for _ in range(self.threshold - 1)]
            coefficients.append(secret)  # Add the secret as the constant term
            logging.info(f'Polynomial coefficients generated: {coefficients}')
            return coefficients
        except Exception as e:
            logging.error(f"Error generating coefficients: {e}")
            raise

    def generate_shares(self, secret):
        """
        Splits the secret into `num_shares` shares using the Shamir Secret Sharing scheme.
        At least `threshold` shares are required to reconstruct the secret.
        """
        try:
            coefficients = self.generate_coefficients(secret)
            shares = [(x, self.polynom(x, coefficients)) for x in random.sample(range(1, FIELD_SIZE), self.num_shares)]
            logging.info(f'{self.num_shares} shares successfully generated.')
            return shares
        except Exception as e:
            logging.error(f"Error generating shares: {e}")
            raise


class PasswordGenerator:
    @staticmethod
    def generate_random_password(length=10):
        """
        Generates a random numeric password of the given length.
        """
        try:
            password = "".join(random.choices(string.digits, k=length))
            logging.info(f'Random password generated: {password}')
            return password
        except Exception as e:
            logging.error(f"Error generating random password: {e}")
            raise


def main():
    try:
        # Generate a random numeric password
        password_gen = PasswordGenerator()
        random_password = password_gen.generate_random_password()

        # Display the generated password
        logging.info(f'Generated Password: {random_password}')

        # Convert password to an integer for secret sharing
        secret = int(random_password)
        logging.info(f'Original Secret (as integer): {secret}')

        # Define the (threshold, number of shares) for secret sharing
        threshold, num_shares = 3, 5

        # Initialize the SecretSharing class
        secret_sharing = SecretSharing(threshold, num_shares)

        # Phase I: Generate shares
        shares = secret_sharing.generate_shares(secret)
        logging.info(f'Shares: {", ".join(str(share) for share in shares)}')

        # Phase II: Secret Reconstruction using `threshold` random shares
        selected_shares = random.sample(shares, threshold)
        logging.info(f'Selected Shares for Reconstruction: {", ".join(str(share) for share in selected_shares)}')
        
        # Reconstruct the secret
        reconstructed_secret = secret_sharing.reconstruct_secret(selected_shares)
        logging.info(f'Reconstructed Secret: {reconstructed_secret}')

    except Exception as e:
        logging.error(f"An error occurred in the main execution flow: {e}")
        raise


if __name__ == "__main__":
    main()
