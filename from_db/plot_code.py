from matplotlib import pyplot as plt


def plot_columns(df,j):
    # Create a larger square-shaped plot
    plt.figure(figsize=(8, 8))

    for column in df.columns:
        plt.plot(df.index, df[column], label=column)




    plt.xlabel('committe_size in percentage')  # Customize the x-axis label as needed
    plt.ylabel('similarity in percentage')  # Customize the y-axis label as needed
    plt.title(f'{j}')  # Customize the plot title as needed
    plt.legend()  # Adjust legend position

    # Adjust layout to prevent overlapping elements
    plt.tight_layout()
    plt.savefig(f'{j}_plot.png')
    # Show the plot
    plt.show()