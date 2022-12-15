import numpy as np
import matplotlib.pyplot as plt

fname = "./ll_no_dropout_nums.txt"

train_data = np.loadtxt(fname=fname)
epochs = train_data[0::3]
accuracy = train_data[1::3]
loss = train_data[2::3]

# print("epochs:", epochs)
# print("accuracy:", accuracy)
# print("loss:", loss)

fig  = plt.figure()
plt.plot(epochs, accuracy, color="blue")
plt.xlabel("epochs")
plt.ylabel("training accuracy")
plt.title("Multi-Linear No Dropout Training Accuracy over 50 Epochs")
plt.savefig('ll_no_dropout_acc_fig.png')


fig = plt.figure()
plt.plot(epochs, loss, color="red")
plt.xlabel("epochs")
plt.ylabel("training loss")
plt.title("Multi-Linear No Dropout Training Loss over 50 Epochs")
plt.savefig('ll_no_dropout_loss_fig.png')


plt.show()