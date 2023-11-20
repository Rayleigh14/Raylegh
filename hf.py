import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor

def get_mac_address():
    # Get the MAC address of the active network adapter on Windows
    if platform.system().lower() == 'windows':
        try:
            result = subprocess.run(
                ['powershell', '(Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Select-Object -First 1).MacAddress'],
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr.strip()}"
    else:
        raise NotImplementedError("This script is designed for Windows only.")

def run_powershell(process_number, batch_number):
    # Path to the PowerShell executable
    powershell_exe_path = r'nom.exe'

    # Build the PowerShell command
    powershell_command = [powershell_exe_path]

    print(f"Executing Process {process_number}, Batch {batch_number} with command: {powershell_command}")

    # Run PowerShell and capture the output (including both stdout and stderr)
    try:
        result = subprocess.run(powershell_command, capture_output=True, text=True, shell=True)
        output = result.stdout.strip()
        error_output = result.stderr.strip()

        # Print output and error if any
        if output:
            print(f"Output for Process {process_number}, Batch {batch_number}:\n{output}")
        if error_output:
            print(f"Error in Process {process_number}, Batch {batch_number}:\n{error_output}")

        return f"Process {process_number}, Batch {batch_number}:\n{output}"
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip()
        print(f"Error in Process {process_number}, Batch {batch_number}:\n{error_output}")
        return f"Error in Process {process_number}, Batch {batch_number}:\n{error_output}"

def run_concurrent_processes(num_processes, num_batches):
    # Calculate the total number of processes
    total_processes = num_processes * num_batches

    # List to store the output of each process
    process_outputs = []

    # Run PowerShell concurrently
    with ThreadPoolExecutor(max_workers=total_processes) as executor:
        # Pass batch numbers to the executor.map function and collect the output
        process_outputs = list(executor.map(run_powershell, range(1, total_processes + 1), [(i // num_processes) + 1 for i in range(total_processes)]))

    # Sort the outputs based on process and batch numbers
    process_outputs.sort(key=lambda x: (int(x.split(",")[0].split()[-1].split(":")[0]), int(x.split(",")[1].split()[-1].split(":")[0])))

    # Save the output to a file
    with open("output.txt", "w") as file:
        file.write("\n".join(process_outputs))

    print("Execution completed. Output saved to 'output.txt'.")

def get_allowed_mac_addresses():
    # List of allowed MAC addresses
    return [
        'write your mac-adress',  #---------------------------------------
    ]

def main():
    print("Welcome to the PowerShell Script Runner!")
    print("----------------------------------------")

    # Get the MAC address
    mac_address = get_mac_address()

    # Display the MAC address
    print(f"Your MAC address is: {mac_address}")

    # Check if the MAC address is authorized
    allowed_mac_addresses = get_allowed_mac_addresses()
    authorized_mac = mac_address in allowed_mac_addresses

    if authorized_mac:
        # Get user input for the number of processes and batches
        num_processes = int(input("Enter the number of processes: "))
        num_batches = int(input("Enter the number of batches: "))

        # Run PowerShell concurrently with the specified number of processes and batches
        run_concurrent_processes(num_processes, num_batches)
    else:
        print("MAC address not authorized.")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
