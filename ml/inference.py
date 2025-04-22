import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import os

# Load ImageNet class labels (only once)
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS_PATH = "imagenet_classes.txt"

if not os.path.exists(LABELS_PATH):
    import urllib.request
    urllib.request.urlretrieve(LABELS_URL, LABELS_PATH)

with open(LABELS_PATH) as f:
    LABELS = [line.strip() for line in f.readlines()]

# Load model once
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = resnet50(weights='ResNet50_Weights.IMAGENET1K_V1').to(device)
model.eval()

# Define preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def predict(file_path: str, topk=1) :
    """Run ResNet50 inference on a PIL Image and return top-k labels."""
    try:
        # Open the image file
        image = Image.open(file_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error opening or processing image {file_path}: {e}")
        return []
    img_transformed = transform(image)
    img_tensor = torch.Tensor(img_transformed).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
        topk_probs, topk_indices = torch.topk(probs, topk)

    predictions = []
    for i in range(topk):
        predictions.append({
            "label": LABELS[topk_indices[i]],
            "confidence": round(topk_probs[i].item(), 4)
        })
    # predictions = predictions[0]
    return predictions
