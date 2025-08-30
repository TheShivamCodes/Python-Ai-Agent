'''
    from functions.get_files_info import get_files_info

def run_tests():
    print('get_files_info("calculator", "."):')
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()

    print('get_files_info("calculator", "pkg"):')
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()

    print('get_files_info("calculator", "/bin"):')
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()

    print('get_files_info("calculator", "../"):')
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    print()

if __name__ == "__main__":
    run_tests()
'''

'''
from functions.get_file_content import get_file_content

def run_tests():
    print('get_file_content("calculator", "main.py"):')
    print(get_file_content("calculator", "main.py"))
    print("\n---\n")

    print('get_file_content("calculator", "pkg/calculator.py"):')
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n---\n")

    print('get_file_content("calculator", "/bin/cat"):')
    print(get_file_content("calculator", "/bin/cat"))
    print("\n---\n")

    print('get_file_content("calculator", "pkg/does_not_exist.py"):')
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print("\n---\n")

if __name__ == "__main__":
    run_tests()
'''

'''
from functions.write_file import write_file

def run_tests():
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("\n---\n")

    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("\n---\n")

    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print("\n---\n")

if __name__ == "__main__":
    run_tests()
'''

from functions.run_python import run_python_file

def run_tests():
    print('run_python_file("calculator", "main.py"):')
    print(run_python_file("calculator", "main.py"))
    print("\n---\n")

    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n---\n")

    print('run_python_file("calculator", "tests.py"):')
    print(run_python_file("calculator", "tests.py"))
    print("\n---\n")

    print('run_python_file("calculator", "../main.py"):')
    print(run_python_file("calculator", "../main.py"))
    print("\n---\n")

    print('run_python_file("calculator", "nonexistent.py"):')
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n---\n")

if __name__ == "__main__":
    run_tests()
