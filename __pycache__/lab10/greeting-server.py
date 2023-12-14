# Import the Pyro4 library for Pyro-based distributed computing.
import Pyro4

@Pyro4.expose
class GreetingMaker:

    # Define a method for generating a greeting message based on the provided name.
    def get_greeting(self, name):
        return f"Hello, {name}. Here is your fortune message: 'Behold the warranty, the bold print giveth and the fine print taketh away.'"

# Define the main function, the entry point of the server application.
def main():
    try:
        daemon = Pyro4.Daemon()
        uri = daemon.register(GreetingMaker)

        # Use Pyro4 to locate the Pyro nameserver, which is responsible for registering and finding Pyro objects.
        with Pyro4.locateNS() as ns:
            ns.register("example.greeting", uri)

        # Print a message indicating that the server is ready and provide the object's URI.
        print("Server is ready. Object URI =", uri)

        # Start the Pyro daemon's request processing loop to handle remote method calls.
        daemon.requestLoop()
    except Pyro4.errors.NamingError:

        # Handle the case where the Pyro nameserver cannot be located.
        print("Error: Failed to locate the Pyro4 nameserver. Make sure the nameserver is running.")
    except Pyro4.errors.PyroError as e:

        # Handle Pyro-specific errors that may occur during execution.
        print(f"Pyro4 Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Check if the script is being run as the main program.
if __name__ == "__main__":
    main()
