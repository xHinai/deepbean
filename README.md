# ☕ Coffee Roasting & Cupping App

A professional web application for coffee roasters to track their roasts and cupping scores using FastAPI and Streamlit. This app follows Specialty Coffee Association (SCA) standards for coffee evaluation.

## ✨ Features

### 🔥 Roast Recording
- Log coffee roast details including:
  - Coffee name and roast date
  - Agtron scores (whole bean and ground)
  - Drop temperature
  - Development time and total time
  - Development Time Ratio (DTR)
  - Roast notes

### 📋 Coffee Cupping
- Score coffees using SCA standards:
  - Fragrance/Aroma
  - Flavor
  - Aftertaste
  - Acidity
  - Body
  - Uniformity
  - Clean Cup
  - Sweetness
  - Overall impression
  - Defects calculation
  - Total score computation

### 📊 Data Management
- View complete roasting history
- Access cupping score records
- Filter data by coffee name and date range
- Export data to CSV format
- Detailed notes and comments storage

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/coffee-app.git
cd coffee-app
```

2. Create a virtual environment and activate it:
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

## 💻 Usage

1. Start the FastAPI backend:
```bash
uvicorn app.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app/frontend.py
```

3. Open your browser and navigate to:
   - Frontend: http://localhost:8501
   - API docs: http://localhost:8000/docs

## 📁 Project Structure 
coffee-app/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI backend
│ ├── models.py # Data models
│ ├── frontend.py # Streamlit interface
│ └── init_db.sql # Database schema
├── requirements.txt # Project dependencies
├── init_db.py # Database initialization
├── .gitignore # Git ignore rules
└── README.md # Project documentation


## 🛠️ Technical Details

### Backend (FastAPI)
- RESTful API endpoints for:
  - Creating and retrieving roast records
  - Storing and fetching cupping scores
  - Data management operations

### Frontend (Streamlit)
- Interactive web interface with:
  - Navigation sidebar
  - Form validation
  - Real-time calculations
  - Data visualization
  - Export functionality

### Database (SQLite)
- Tables:
  - `coffee_roasts`: Stores roasting data
  - `coffee_scores`: Stores cupping scores
  - Relational linking between roasts and scores

## 📊 Data Models

### Roast Record
```python
class CoffeeRoast:
    roast_id: str
    date: datetime
    coffee_name: str
    agtron_whole: int
    agtron_ground: int
    drop_temp: float
    development_time: float
    total_time: float
    dtr_ratio: float
    notes: Optional[str]
```

### Cupping Score
```python
class CoffeeScore:
    score_id: str
    roast_id: str
    date: datetime
    fragrance_aroma: float
    flavor: float
    aftertaste: float
    acidity: float
    body: float
    uniformity: float
    clean_cup: float
    sweetness: float
    overall: float
    defects: int
    total_score: float
    notes: Optional[str]
```

## 🔄 API Endpoints

- `POST /roasts/`: Create a new roast record
- `GET /roasts/`: Retrieve all roast records
- `POST /scores/`: Create a new cupping score
- `GET /scores/`: Retrieve all cupping scores

## 🎯 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Data visualization and analytics
- [ ] Green coffee inventory management
- [ ] Roast profile curves
- [ ] Custom scoring templates
- [ ] Batch tracking
- [ ] Export to PDF format
- [ ] Mobile responsiveness

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Specialty Coffee Association (SCA) for cupping standards
- FastAPI team for the amazing framework
- Streamlit team for making data apps easy to build

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/coffee-app](https://github.com/yourusername/coffee-app)