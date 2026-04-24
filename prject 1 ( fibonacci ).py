# prject 1 

import math 

def generate_fibonacci(n):
    """Generate and print the first n Fibonacci numbers."""
    if n <= 0:
        print("Please enter a positive integer.")
        return
    
    print(f"The first {n} Fibonacci numbers are:")
    a, b = 0, 1
    for i in range(n):
        print(f"{i + 1}: {a}")
        a, b = b, a + b

def is_perfect_square(num):
    """Check if a number is a perfect square."""
    if num < 0:
        return False
    root = int(math.sqrt(num))
    return root * root == num        

def is_fibonacci(num):
    """ 
    A number is Fibonacci if one of those is a perfect square:
    5*num*num + 4 or 5*num*num - 4
    
    """

    if num < 0:
        return False
    return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)

def check_fibonacci():
    """ 
    Ask user for a number and check if it's a Fibonacci sequence number
    
    """
    try:
        num = int(input("Enter a number to check if it's a Fibonacci number: "))
        if is_fibonacci(num):
            print(f"{num} is a Fibonacci number.")
        else:
            print(f"{num} is not a Fibonacci number.")
    except ValueError:
        print("Please enter a valid integer.")

def show_menu():
    """Display the menu options."""
    print("\nMenu:")
    print("1. Generate Fibonacci numbers")
    print("2. Check if a number is a Fibonacci number")
    print("3. Exit")        
    
def main():
    print("Welcome to the Fibonacci Sequence Generator and Checker!")
    
    while True:
        show_menu()
        choice = input("Please select an option (1, 2, or 3): ")
        
        if choice == '1':
            try:
                n = int(input("How many Fibonacci numbers would you like to generate? "))
                generate_fibonacci(n)
            except ValueError:
                print("Please enter a valid integer.")
        elif choice == '2':
            check_fibonacci()
        elif choice == '3':
            print("Thank you for using the Fibonacci Sequence Generator and Checker. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")    

if __name__ == "__main__":
    main()            