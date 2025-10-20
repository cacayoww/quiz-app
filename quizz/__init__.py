from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = '2cabb2b9ce7e4297c17ab545'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

# set default redirect untuk login_required
login_manager.login_view = '/'  # ganti ke route yang kamu mau
def create_tables():
    with app.app_context():
        db.create_all()

def add_quiz_questions():
    from quizz.models import Quiz
    with app.app_context():
        if Quiz.query.first():
            return
        
        q1 = Quiz(
            question='Di bawah ini adalah library Python yang dipakai untuk pengembangan kecerdasan buatan, kecuali...',
            option_a='Tensorflow',
            option_b='Scikit-Learn',
            option_c='Pandas',
            option_d='Pickle',
            correct_answer='D'
        )
        q2 = Quiz(
            question='Pandas adalah library Python yang berguna untuk mengolah data tabular yang disebut dengan?',
            option_a='DataFrame',
            option_b='DataTable',
            option_c='DataRow',
            option_d='DataColumn',
            correct_answer='A'
        )
        q3 = Quiz(
            question='Library Python di bawah ini yang dapat dipakai untuk melatih model Machine Learning adalah?',
            option_a='Scikit-Learn',
            option_b='Matplotlib',
            option_c='Pandas',
            option_d='Numpy',
            correct_answer='A'
        )
        q4 = Quiz(
            question='Library Python di bawah ini yang dapat dipakai untuk melakukan visualisasi data pada tahap Exploratory Data Analysis adalah?',
            option_a='Tensorflow',
            option_b='Matplotlib',
            option_c='Pandas',
            option_d='Numpy',
            correct_answer='B'
        )
        q5 = Quiz(
            question='Algoritma di bawah ini yang menangani tugas supervised learning adalah?',
            option_a='SVM',
            option_b='K-Means',
            option_c='DBSCAN',
            option_d='GaussianMixture',
            correct_answer='A'
        )
        q6 = Quiz(
            question='Algoritma di bawah ini yang menangani tugas klasifikasi adalah?',
            option_a='Logistic Regression',
            option_b='Linear Regression',
            option_c='Ridge',
            option_d='SVR',
            correct_answer='A'
        )
        q7 = Quiz(
            question='Import Data pada Python dapat dilakukan dengan menggunakan library?',
            option_a='Matplotlib',
            option_b='Numpy',
            option_c='Scikit-Learn',
            option_d='Pandas',
            correct_answer='D'
        )
        q8 = Quiz(
            question='Di bawah ini adalah algoritma clustering, kecuali?',
            option_a='KMeans',
            option_b='DBSCAN',
            option_c='Ridge',
            option_d='Birch',
            correct_answer='C'
        )
        q9 = Quiz(
            question='Metode evaluasi model yang umum digunakan untuk mengukur performa model klasifikasi adalah?',
            option_a='Mean Squared Error',
            option_b='Accuracy Score',
            option_c='R2 Score',
            option_d='Silhouette Score',
            correct_answer='B'
        )
        q10 = Quiz(
            question='Fungsi utama dari library NumPy dalam Python adalah?',
            option_a='Manipulasi array dan operasi numerik',
            option_b='Visualisasi data',
            option_c='Pembuatan model Machine Learning',
            option_d='Manipulasi data tabular',
            correct_answer='A'
        )
        q11 = Quiz(
            question='Proses membagi dataset menjadi data latih dan data uji disebut dengan?',
            option_a='Normalization',
            option_b='Standardization',
            option_c='Train-Test Split',
            option_d='Cross Validation',
            correct_answer='C'
        )
        q12 = Quiz(
            question='Library Python yang digunakan untuk membuat model deep learning adalah?',
            option_a='Seaborn',
            option_b='TensorFlow',
            option_c='Matplotlib',
            option_d='Statsmodels',
            correct_answer='B'
        )
        q13 = Quiz(
            question='Tahapan awal dalam proyek data science yang biasanya dilakukan pertama kali adalah?',
            option_a='Model Deployment',
            option_b='Data Cleaning',
            option_c='Model Training',
            option_d='Hyperparameter Tuning',
            correct_answer='B'
        )
        q14 = Quiz(
            question='Metode unsupervised learning yang digunakan untuk mengelompokkan data berdasarkan kemiripan disebut?',
            option_a='Classification',
            option_b='Regression',
            option_c='Clustering',
            option_d='Dimensionality Reduction',
            correct_answer='C'
        )
        q15 = Quiz(
            question='Teknik yang digunakan untuk mengubah data kategori menjadi bentuk numerik agar bisa digunakan oleh model Machine Learning adalah?',
            option_a='Feature Scaling',
            option_b='One-Hot Encoding',
            option_c='Normalization',
            option_d='Data Imputation',
            correct_answer='B'
        )

        db.session.add(q1)
        db.session.add(q2)
        db.session.add(q3)
        db.session.add(q4)
        db.session.add(q5)
        db.session.add(q6)
        db.session.add(q7)
        db.session.add(q8)
        db.session.add(q9)
        db.session.add(q10)
        db.session.add(q11)
        db.session.add(q12)
        db.session.add(q13)
        db.session.add(q14)
        db.session.add(q15)

        db.session.commit()

def init_database():
    create_tables()
    add_quiz_questions()

from quizz import routes