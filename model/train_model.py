import torch
import torchvision
from torchvision import datasets, transforms
from torch import nn, optim
import os

def load_data(data_dir, train=True):
    # Apply different transformations for training and testing
    if train:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),  # Data augmentation
            transforms.RandomRotation(10),      # Random rotation
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=train)
    return dataloader

def build_model(num_classes):
    model = torchvision.models.resnet18(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    return model

def train_model(model, dataloader, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.003)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)  # Learning rate scheduler

    for epoch in range(epochs):
        model.train()  # Set the model to training mode
        running_loss = 0.0

        for inputs, labels in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        scheduler.step()  # Update the learning rate
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(dataloader)}")

    torch.save(model.state_dict(), 'trained_model.pt')

def test_model(model, test_loader):
    model.eval()  # Set the model to evaluation mode
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f'Accuracy of the model on test images: {accuracy}%')

if __name__ == "__main__":
    train_data_dir = './app/static/train-data'
    test_data_dir = './app/static/test-data'
    num_classes = 10  # Update with the actual number of classes

    train_dataloader = load_data(train_data_dir, train=True)
    test_dataloader = load_data(test_data_dir, train=False)

    model = build_model(num_classes)
    train_model(model, train_dataloader)
    test_model(model, test_dataloader)
