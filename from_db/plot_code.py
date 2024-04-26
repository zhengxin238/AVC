from matplotlib import pyplot as plt


def plot_columns(df,j):
    # Create a larger square-shaped plot
    plt.figure(figsize=(8, 8))

    for column in df.columns:
        plt.plot(df.index, df[column], label=column)




    plt.xlabel('commitee_size')  # Customize the x-axis label as needed
    plt.ylabel('spercentage_of_best_value')  # Customize the y-axis label as needed
    plt.title(f'{j}')  # Customize the plot title as needed
    plt.legend()  # Adjust legend position

    # Adjust layout to prevent overlapping elements
    plt.tight_layout()
    plt.savefig(f'{j}_plot.png')
    # Show the plot
    plt.show()


def plot_row(df,j):
    # Create a larger square-shaped plot
    plt.figure(figsize=(8, 8))

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        plt.plot(row, label=index)  # Plot each row with a label

    # Set the y-axis limits to range from 0 to 1
    plt.ylim(0, 1)

    # Set aspect ratio to be equal (to make the plot square)
    plt.gca().set_aspect('equal', adjustable='box')

    # Add labels and legend
    plt.xlabel('rising_p')
    plt.ylabel('percentage_of_best_value')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Adjust legend position
    plt.title(f"{j}")
    # Adjust layout to prevent overlapping elements
    plt.tight_layout()
    plt.savefig(f"row{j}.png")
    # Show the plot
    plt.show()