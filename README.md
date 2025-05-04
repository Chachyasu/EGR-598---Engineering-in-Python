# EGR-598 Engineering-in-Python
Final project 

This Streamlit app generates and visualizes a real-time sine wave based on user-defined amplitude and frequency inputs. It simulates continuous wave motion by calculating time-scaled sine values and updating them dynamically at a defined interval. The resulting data is plotted with high-quality rendering and written to a CSV file, which is overwritten on each update to store only the current visible time window. Users can reset the session, view the latest data point, or toggle to display a full data history. The visualization is styled for clarity, with smooth animation and performance optimizations to ensure consistent updates.

![image](https://github.com/user-attachments/assets/89c7bc19-46d6-4a17-9093-4008e0651fe2)

The streamlit app will ask the user two inputs needed to modify the graph which are the frequency and the amplitude, when either the parameters are changed the graph will dynamically change at the split second the user input the number. 

This is the graph with 0 amplitude and frequency
![image](https://github.com/user-attachments/assets/a0522af2-6780-4bc0-b5f9-46faab3e255d)

This is the graph with different inputs
![image](https://github.com/user-attachments/assets/b78b1080-e15e-4ed4-8c8e-6adff520bcc1)

The streamlit app also comes with a table that shows the latest data points generated for the user to see what's the exact number of the data point that has been generated and an option to view the full history
![image](https://github.com/user-attachments/assets/c757af88-c324-4e02-9521-c5f385015470)

Full Data generated history
![image](https://github.com/user-attachments/assets/2712b3bd-9540-441a-9ffd-570e8ce97c55)

The user can import the CSV file generated which the data points generated can be view in the table prior download


