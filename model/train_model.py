import torch
import torchvision
from torchvision import datasets, transforms
from torch import nn, optim
import os

def load_data(data_dir):
    # Data transformation and augmentation
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # Load dataset
    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
    return dataloader

def build_model():
    # Using a pre-trained model and modifying it
    model = torchvision.models.resnet18(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)  # Adjust for your number of classes
    return model

def train_model(model, dataloader, epochs=10):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.003)

    for epoch in range(epochs):
        for inputs, labels in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item()}")

    torch.save(model.state_dict(), 'trained_model.pt')

if __name__ == "__main__":
    data_dir = '/app/static/train-data'
    num_classes = 10  # spaghetti, biryani, cake, sushi, soup, poke, paella, tacos, ramen, salad

    dataloader = load_data(data_dir)
    model = build_model()
    train_model(model, dataloader)
