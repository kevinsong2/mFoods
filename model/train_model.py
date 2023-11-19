import torch
import torchvision
from torchvision import datasets, transforms, models
from torch import nn, optim

from sklearn import metrics
import os

def load_data(data_dir, train=True):
    if train:
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
    else:
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    dataset = datasets.ImageFolder(root=data_dir, transform=transform)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=train)
    return dataloader

def build_model(num_classes):
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    return model

def train_model(model, dataloader, epochs=8):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    # scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for inputs, labels in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # scheduler.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss / len(dataloader)}")

    torch.save(model.state_dict(), 'trained_model.pt')

def test_model(model, test_loader):
    print("start test")
    model.eval()
    correct = 0
    total = 0
    y_true = []
    y_pred = []
    y_score = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            y_true.extend(labels)
            predicted = torch.argmax(outputs.data, dim=1)
            y_pred.extend(predicted)
            y_score.extend(nn.functional.softmax(outputs.data, dim=1))
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    auroc = metrics.roc_auc_score(y_true, y_score, multi_class="ovo")
    accuracy = 100 * (correct / total)
    print(f'Accuracy of the model on test images: {accuracy}% and a ROC AUC score: {auroc}')

if __name__ == "__main__":
    train_data_dir = './app/static/train-data'
    test_data_dir = './app/static/test-data'
    num_classes = 3 # Update this based on your dataset
    premodel = "trained_model.pt"

    train_dataloader = load_data(train_data_dir, train=True)
    test_dataloader = load_data(test_data_dir, train=False)

    if os.path.exists(premodel):
        model = build_model(num_classes)
        model.load_state_dict(torch.load(premodel))
        model.eval()
        # train_model(model, train_dataloader)
    else:
        print("no pretrained model")
        model = build_model(num_classes)
        train_model(model, train_dataloader)
    test_model(model, test_dataloader)