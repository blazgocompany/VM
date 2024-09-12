import psutil

def get_system_info():
    # Get total RAM in GB
    total_ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB

    # Get number of CPUs
    num_cpus = psutil.cpu_count(logical=True)  # logical=True to include hyper-threaded CPUs

    print(f"Total RAM: {total_ram:.2f} GB")
    print(f"Number of vCPUs: {num_cpus}")

if __name__ == "__main__":
    get_system_info()
