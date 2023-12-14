# Import the Pyro4 library, which is used for remote procedure calls (RPC).
import Pyro4

# Define the main function, the entry point of the program.
def main():

    # Prompt the user to enter a Pyro URI for the greeting object
    uri = input("Enter the Pyro URI of the greeting object: ").strip()

    # Prompt the user to enter their name
    name = input("Enter your name: ").strip()

    # Create a Pyro4 Proxy object named greeting_maker to interact with the remote Pyro object identified by the given URI.
    greeting_maker = Pyro4.Proxy(uri)

    # This method is expected to return a greeting message from the remote object.
    greeting_message = greeting_maker.get_greeting(name)
    print(greeting_message)

# Check if the script is being run as the main program.
if __name__ == "__main__":
    main()
