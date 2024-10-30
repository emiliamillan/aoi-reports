def find_duplicates(numbers):
    # Create a dictionary to count occurrences of each number
    counts = {}
    for number in numbers:
        if number in counts:
            counts[number] += 1
        else:
            counts[number] = 1
    
    # Extract numbers that appear more than once
    duplicates = [num for num, count in counts.items() if count > 1]
    return duplicates

# Input: range of numbers separated by commas
numbers = list(map(int, input("Enter numbers separated by commas: ").split(',')))

# Find duplicates
duplicates = find_duplicates(numbers)

# Output the duplicates
print("Duplicates:", duplicates)


