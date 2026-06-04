import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import joblib
import os
from tensorflow.keras.models import load_model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

#Load dataset
df = pd.read_csv("student_mental_health_clean.csv")

# Load Model
@st.cache_resource
def load_model_assets():
    burnout_model = load_model("burnout_model.keras")
    mental_health_model = load_model("mental_health_model.keras")
    scaler = joblib.load("scaler.save")
    return burnout_model, mental_health_model, scaler

burnout_model, mental_health_model, scaler = load_model_assets()

# Membuat fungsi visualisasi
def visualisasi_variabel_utama(df,col):
    """
    Fungsi untuk menampilkan variabel utama berdasarkan kolom variabel 
    yang dipilih pada streamlit
    """
    # Statistik Dasar
    mean_val = df[col].mean()
    min_val = df[col].min()
    max_val = df[col].max()

    # Membuat plot
    fig = px.histogram(df[col],title=f"Histogram {col}")

    fig.update_layout(
        xaxis_title=col,
        yaxis_title="Frekuensi",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Menampilkan Statistik Dasar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Rata - Rata",value=f"{mean_val:.2f}")
    with col2:
        st.metric(label="Nilai minimum",value=f"{min_val:.2f}")
    with col3:
        st.metric(label="Nilai maksimum",value=f"{max_val:.2f}")

def visualisasi_berdasarkan_risk_level(df,col):
    """
    Fungsi untuk menampilkan rata - rata kolom variabel yang dipilih 
    berdasarkan kategori risiko burnout (risk_level) pada streamlit
    """
    # Menyortir data berdasarkan risk level
    risk_comparison = df.groupby("risk_level")[col].mean().reset_index()

    # Memperbaiki urutan kategori yang akan ditampilkan
    risk_order = ["Low", "Medium", "High"]
    risk_comparison["risk_level"] = pd.Categorical(
    risk_comparison["risk_level"],
    categories=risk_order,
    ordered=True
    )

    risk_comparison = risk_comparison.sort_values("risk_level")
    # Membuat plot
    fig = px.bar(
        risk_comparison,
        x="risk_level",
        y=col,
        text=risk_comparison[col].round(2),
        category_orders={"risk_level": risk_order},
        title=f"Rata-rata {col} berdasarkan Risiko Burnout"
    )

    fig.update_layout(
        xaxis_title="Risk Level",
        yaxis_title=f"Rata-rata {col}",
        height=500
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

def visualisasi_correlation_heatmap(df,col):
    """
    Fungsi untuk menampilkan korelasi antarvariabel 
    numerik dalam dataset pada streamlit
    """
    # Membuat plot
    corr_matrix = df[col].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap",
        zmin=-1,
        zmax=1
    )

    fig.update_layout(
        height=650,
        xaxis_title="Variabel",
        yaxis_title="Variabel"
    )

    st.plotly_chart(fig, use_container_width=True)

def visualisasi_risk_level_demografi(df,demo, mode="Persentase"):
    """
    Fungsi untuk menampilkan distribusi risiko burnout berdasarkan variabel demografi
    seperti gender atau academic_year dalam bentuk persentase atau jumlah data.
    """
    risk_order = ["Low", "Medium", "High"]
    if mode == "Persentase":
        risk_demo = pd.crosstab(
            df[demo],
            df["risk_level"],
            normalize="index"
        ) * 100

        risk_demo = risk_demo.reset_index()

        risk_demo_melted = risk_demo.melt(
            id_vars=demo,
            value_vars=[col for col in risk_order if col in risk_demo.columns],
            var_name="risk_level",
            value_name="persentase"
        )

        fig = px.bar(
            risk_demo_melted,
            x=demo,
            y="persentase",
            color="risk_level",
            text=risk_demo_melted["persentase"].round(1),
            barmode="stack",
            category_orders={"risk_level": risk_order},
            title=f"Proporsi Risiko Burnout berdasarkan {demo}"
        )

        fig.update_layout(
            xaxis_title=f"{demo}",
            yaxis_title="Persentase (%)",
            height=500
        )

    else:
        risk_demo = df.groupby(
            [demo, "risk_level"]
        ).size().reset_index(name="jumlah")

        fig = px.bar(
            risk_demo,
            x=demo,
            y="jumlah",
            color="risk_level",
            text="jumlah",
            barmode="stack",
            category_orders={"risk_level": risk_order},
            title=f"Jumlah Risiko Burnout berdasarkan {demo}"
        )

        fig.update_layout(
            xaxis_title=f"{demo}",
            yaxis_title="Jumlah Data",
            height=500
        )

    st.plotly_chart(fig, use_container_width=True)

def visualisasi_distribusi_risk_level(df):
    """
    Fungsi untuk menampilkan distribusi keseluruhan kategori risk_level,
    meliputi metrik ringkas, bar chart jumlah data, dan donut chart persentase.
    """

    # Menentukan urutan kategori risk level
    risk_order = ["Low", "Medium", "High"]

    # Menghitung jumlah dan persentase
    risk_count = df["risk_level"].value_counts().reindex(risk_order).reset_index()
    risk_count.columns = ["risk_level", "jumlah"]

    risk_count["persentase"] = (
        risk_count["jumlah"] / risk_count["jumlah"].sum() * 100
    ).round(2)

    # Menampilkan metrik ringkas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Low Risk",
            value=f"{risk_count.loc[risk_count['risk_level'] == 'Low', 'persentase'].values[0]}%"
        )

    with col2:
        st.metric(
            label="Medium Risk",
            value=f"{risk_count.loc[risk_count['risk_level'] == 'Medium', 'persentase'].values[0]}%"
        )

    with col3:
        st.metric(
            label="High Risk",
            value=f"{risk_count.loc[risk_count['risk_level'] == 'High', 'persentase'].values[0]}%"
        )

    # Bar chart jumlah data
    fig_bar = px.bar(
        risk_count,
        x="risk_level",
        y="jumlah",
        text="jumlah",
        category_orders={"risk_level": risk_order},
        title="Jumlah Data berdasarkan Risk Level"
    )

    fig_bar.update_layout(
        xaxis_title="Risk Level",
        yaxis_title="Jumlah Data",
        height=450
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # Donut chart persentase
    fig_pie = px.pie(
        risk_count,
        names="risk_level",
        values="jumlah",
        hole=0.45,
        title="Persentase Risk Level"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # Interpretasi
    kategori_terbesar = risk_count.sort_values(
        by="jumlah",
        ascending=False
    ).iloc[0]

def visualisasi_burnout_academic_year(df):
    """
    Fungsi untuk menampilkan rata-rata burnout_score
    berdasarkan tingkat academic_year pada Streamlit.
    """
    # Menghitung rata-rata burnout_score berdasarkan academic_year
    burnout_year = (
        df.groupby("academic_year")["burnout_score"]
        .mean()
        .reset_index()
        .sort_values("academic_year")
    )

    # Membuat label agar lebih mudah dibaca
    burnout_year["academic_year_label"] = (
        "Tahun ke-" + burnout_year["academic_year"].astype(str)
    )

    # Membuat bar chart
    fig = px.bar(
        burnout_year,
        x="academic_year_label",
        y="burnout_score",
        text=burnout_year["burnout_score"].round(2),
        title="Rata-rata Burnout Score berdasarkan Academic Year"
    )

    fig.update_layout(
        xaxis_title="Academic Year",
        yaxis_title="Rata-rata Burnout Score",
        height=500
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)

def visualisasi_daily_features_to_burnout(df):
    """
    Fungsi untuk menampilkan faktor harian yang memiliki hubungan paling kuat
    dengan burnout_score menggunakan korelasi Pearson.
    """  
    # Menentukan faktor harian
    daily_features = [
    "study_hours_per_day",
    "exam_pressure",
    "academic_performance",
    "stress_level",
    "anxiety_score",
    "depression_score",
    "sleep_hours",
    "physical_activity",
    "social_support",
    "screen_time",
    "internet_usage",
    "financial_stress",
    "family_expectation"
    ]
    daily_features = [col for col in daily_features if col in df.columns]

    # Menghitung korelasi setiap faktor dengan burnout_score
    corr_data = df[daily_features + ["burnout_score"]].corr()["burnout_score"]
    corr_df = corr_data.reset_index()
    corr_df.columns = ["variabel", "korelasi"]

    # Menambahkan nilai absolut korelasi untuk mengurutkan kekuatan hubungan
    corr_df["korelasi_absolut"] = corr_df["korelasi"].abs()

    corr_df = corr_df.sort_values(
        by="korelasi_absolut",
        ascending=False
    )
    label_variabel = {
    "study_hours_per_day":"Durasi Belajar",
    "exam_pressure":"Tekanan Ujian",
    "academic_performance": "Performa Akademik",
    "stress_level":"Tingkat Stres",
    "anxiety_score":"Skor Kecemasan (anxiety)",
    "depression_score":"Skor Depresi",
    "sleep_hours":"Durasi Tidur per Hari",
    "physical_activity": "Aktivitas Fisik",
    "social_support": "Dukungan Sosial",
    "screen_time": "Screen Time",
    "internet_usage": "Penggunaan Internet",
    "financial_stress": "Tekanan Finansial",
    "family_expectation": "Ekspektasi Keluarga"
    }

    corr_df["nama_variabel"] = corr_df["variabel"].map(label_variabel)

    # Membuat plot
    fig = px.bar(
        corr_df,
        x="korelasi",
        y="nama_variabel",
        orientation="h",
        text=corr_df["korelasi"].round(2),
        title="Faktor Harian dengan Hubungan Terkuat terhadap Burnout Score"
    )

    fig.update_layout(
        xaxis_title="Nilai Korelasi dengan Burnout Score",
        yaxis_title="Faktor Harian",
        height=600
    )

    fig.update_traces(
        textposition="outside"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

def visualisasi_profil_kondisi_harian_risk_level(df):
    """
    Fungsi untuk menampilkan profil rata-rata kondisi harian mahasiswa
    berdasarkan kategori risk_level.
    """

    conditions = [
        "stress_level",
        "exam_pressure",
        "sleep_hours",
        "physical_activity",
        "social_support",
        "screen_time"
    ]

    # Menghitung rata-rata setiap variabel berdasarkan risk_level
    profil_df = df.groupby("risk_level")[conditions].mean().reset_index()

    # Mengatur urutan risk_level
    risk_order = ["Low", "Medium", "High"]

    profil_df["risk_level"] = pd.Categorical(
        profil_df["risk_level"],
        categories=risk_order,
        ordered=True
    )

    profil_df = profil_df.sort_values("risk_level")

    # Mengubah format data dari wide ke long agar cocok untuk px.bar
    profil_melted = profil_df.melt(
        id_vars="risk_level",
        value_vars=conditions,
        var_name="variabel",
        value_name="rata_rata"
    )

    # Label agar lebih mudah dibaca
    label_variabel = {
        "stress_level": "Tingkat Stres",
        "exam_pressure": "Tekanan Ujian",
        "sleep_hours": "Durasi Tidur per Hari",
        "physical_activity": "Aktivitas Fisik",
        "social_support": "Dukungan Sosial",
        "screen_time": "Screen Time"
    }

    profil_melted["nama_variabel"] = profil_melted["variabel"].map(label_variabel)

    # Membuat plot
    fig = px.bar(
        profil_melted,
        x="nama_variabel",
        y="rata_rata",
        color="risk_level",
        barmode="group",
        text=profil_melted["rata_rata"].round(2),
        category_orders={
            "risk_level": risk_order,
            "nama_variabel": list(label_variabel.values())
        },
        title="Profil Kondisi Harian Berdasarkan Risiko Burnout"
    )

    fig.update_layout(
        xaxis_title="Variabel Harian",
        yaxis_title="Rata-rata Nilai",
        legend_title="Risk Level",
        height=600
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(fig, use_container_width=True)
    
def visualisasi_hubungan_target_utama(df):
    """
    Fungsi untuk menampilkan hubungan antara burnout_score,
    mental_health_index, dan dropout_risk.
    """
    # Membentuk matriks
    target  = ["burnout_score","mental_health_index","dropout_risk"]
    corr_matrix = df[target].corr()
    
    # Membuat Heatmap korelasi
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap antara Burnout, Mental Health, dan Dropout Risk",
        zmin=-1,
        zmax=1
    )

    fig_heatmap.update_layout(
        height=500,
        xaxis_title="Variabel",
        yaxis_title="Variabel"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Membuat tabel korelasi pasangan variabel
    pair_corr = pd.DataFrame({
        "pasangan_variabel": [
            "Burnout Score vs Mental Health Index",
            "Burnout Score vs Dropout Risk",
            "Mental Health Index vs Dropout Risk"
        ],
        "korelasi": [
            corr_matrix.loc["burnout_score", "mental_health_index"],
            corr_matrix.loc["burnout_score", "dropout_risk"],
            corr_matrix.loc["mental_health_index", "dropout_risk"]
        ]
    })

    pair_corr["korelasi_absolut"] = pair_corr["korelasi"].abs()

    pair_corr = pair_corr.sort_values(
        by="korelasi_absolut",
        ascending=False
    )

    # Membuat Bar chart korelasi pasangan variabel
    fig_bar = px.bar(
        pair_corr,
        x="korelasi",
        y="pasangan_variabel",
        orientation="h",
        text=pair_corr["korelasi"].round(2),
        title="Kekuatan Hubungan antar Variabel Utama"
    )

    fig_bar.update_layout(
        xaxis_title="Nilai Korelasi",
        yaxis_title="Pasangan Variabel",
        height=450
    )

    fig_bar.update_traces(textposition="outside")
    fig_bar.update_yaxes(autorange="reversed")

    st.plotly_chart(fig_bar, use_container_width=True)

# Membuat konfigurasi halaman
st.set_page_config(
    page_title="Student Burnout Risk & Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Membuat sidebar
if "page" not in st.session_state:
    st.session_state.page = "📈 Visualisasi Data"


with st.sidebar:
    st.title("Student Burnout Risk & Mental Health Dashboard Menu")
    

    if st.button("📈 Visualisasi Data",use_container_width=True):
        st.session_state.page = "📈 Visualisasi Data"

    if st.button("📝 Prediksi Risiko Burnout",use_container_width=True):
        st.session_state.page = "📝 Prediksi Risiko Burnout"

    st.markdown("---")
    st.info("💡 **Tips:** Gunakan halaman visualisasi untuk memahami data, dan halaman prediksi untuk mengetahui risiko burnout dengan bantuan AI.")

# Halaman visualisasi data
if st.session_state.page == "📈 Visualisasi Data":
    st.title("Student Burnout Risk & Mental Health Dashboard")
    st.markdown("""<div style='text-align: justify'>
Dashboard ini berfungsi sebagai media visualisasi interaktif untuk menampilkan ringkasan data, distribusi variabel, statistik deskriptif, 
serta membantu pengguna memahami hubungan umum antarindikator dalam dataset. Student Mental Health and Burnout Dataset digunakan sebagai sumber data mrupakan
dataset sintetis yang menggambarkan hubungan antara tekanan akademik, kebiasaan hidup, perilaku digital, faktor lingkungan, dan kondisi kesehatan mental mahasiswa.
Dataset ini terdiri dari 1.000.000 baris data dan 20 variabel. Selain itu, dashboard ini juga disertai mini quiz sebagai simulasi untuk memprediksi kondisi mental
mahasiswa berdasarkan input pengguna yang dapat menjadi dasar dalam pengembangan sistem prediksi atau pemantauan risiko burnout mahasiswa berbasis data.
    </div>""",unsafe_allow_html=True)
    st.write("\n")
    st.write(df.head())

    # Menampilkan visualisasi utama 
    st.subheader("Distribusi Variabel Utama")
    variabel_utama = {"Tingkat Stres":"stress_level",
                      "Skor Kecemasan (Anxiety)":"anxiety_score",
                      "Skor Depresi":"depression_score",
                      "Tekanan Ujian":"exam_pressure", 
                      "Durasi Tidur per Hari":"sleep_hours",
                      "Durasi Belajar per Hari":"study_hours_per_day",
                      "Tekanan Finansial":"financial_stress", 
                      "Ekspektasi Keluarga":"family_expectation",
                      "Dukungan Sosial":"social_support",
                      "Aktivitas Fisik":"physical_activity",
                      "Skor Burnout":"burnout_score",
                      "Skor Kesehatan Mental":"mental_health_index"
                      }
    var = st.selectbox(
        label="Pilih Variabel yang Ingin Ditampilkan",
        options=list(variabel_utama.keys())
    )
    visualisasi_variabel_utama(df,variabel_utama[var])

    # Menampilkan perbandingan data berdasarkan risk levelnya
    st.subheader("Perbandingan Rata - Rata berdasarkan Risiko Burnout")
    variabel_terpilih = {
        "Tingkat Stress":"stress_level",
        "Skor Kecemasan (Anxiety)":"anxiety_score",
        "Skor Depresi":"depression_score",
        "Tingkat Tekanan Ujian":"exam_pressure", 
        "Durasi Tidur per Hari":"sleep_hours",
        "Durasi Belajar per Hari":"study_hours_per_day",
        "Tingkat Tekanan Finansial":"financial_stress", 
        "Tingkat Ekspektasi Keluarga":"family_expectation",
        "Tingkat Dukungan Sosial":"social_support",
        "Aktivitas Fisik":"physical_activity",
        "Skor Kesehatan Mental":"mental_health_index"
    }
    var_2 = st.selectbox(
        label="Pilih Variabel yang Ingin Ditampilkan",
        options=list(variabel_terpilih.keys())
    )
    visualisasi_berdasarkan_risk_level(df,variabel_terpilih[var_2])

    # Menampilkan heatmap korelasi antar variabel terpilih
    st.subheader("Correlation Heatmap Variabel Utama")
    var_3 = st.multiselect(
       label="Pilih Variabel yang Ingin Ditampilkan",
       options= list(variabel_utama.keys()),
       default= list(variabel_utama.keys())
    )
    if len(var_3) < 2:
        st.warning("Pilih minimal 2 variabel untuk membuat correlation heatmap.")
    else:
        selected_cols = [variabel_utama[column] for column in var_3]
        visualisasi_correlation_heatmap(df,selected_cols)

    # Menampilkan distribusi risiko burnout 
    st.subheader("Distribusi Risiko Burnout Mahasiswa")
    visualisasi_distribusi_risk_level(df)
    with st.expander("Lihat Insight"):
        st.markdown(
        """<div style='text-align: justify'>
        Berdasarkan distribusi risk_level, mayoritas mahasiswa berada pada kategori Low risk dengan 766.645 data atau sekitar 76,66% 
        diikuti Medium risk sebanyak 218.275 data atau sekitar 21,83%, dan High risk sebanyak 15.080 data atau sekitar 1,51%.
        Pola ini menunjukkan bahwa sebagian besar mahasiswa dalam dataset berada pada tingkat risiko burnout rendah. Namun,
        kelompok Medium risk dan High risk tetap perlu diperhatikan karena keduanya merepresentasikan mahasiswa yang menunjukkan
        indikasi risiko burnout lebih tinggi dibandingkan kelompok Low risk. Hasil ini mendukung kebutuhan sistem monitoring burnout mahasiswa,
        karena sistem dapat membantu mahasiswa mengetahui tingkat risikonya secara lebih awal. Kelompok Medium risk dapat menjadi perhatian untuk
        pencegahan dini, sedangkan kelompok High risk dapat menjadi prioritas untuk diberikan peringatan atau rekomendasi tindak lanjut.
        """,unsafe_allow_html=True
        )

    # Menampilkan risiko burnout berdasarkan gender
    st.subheader("Risiko Burnout berdasarkan Gender Mahasiswa")
    mode_gender = st.radio(
    "Tampilkan dalam:",
    options=["Persentase", "Jumlah Data"],
    horizontal=True,
    key="mode_gender"
    )

    visualisasi_risk_level_demografi(df,demo="gender",mode=mode_gender)
    st.info("💡 **Tips:** Setiap batang bernilai total 100%. Warna menunjukkan proporsi Low, Medium, dan High." \
    " Klik legenda di kanan untuk menyembunyikan atau menampilkan kategori tertentu.")

    # Menampilkan risiko burnout berdasarkan tahun akademik
    st.subheader("Risiko Burnout berdasarkan Tahun Akademik Mahasiswa")
    mode_academic_year = st.radio(
    "Tampilkan dalam:",
    options=["Persentase", "Jumlah Data"],
    horizontal=True,
    key="mode_academic_year"
    )  

    visualisasi_risk_level_demografi(df,demo="academic_year",mode=mode_academic_year)

    st.info("💡 **Tips:** Setiap batang bernilai total 100%. Warna menunjukkan proporsi Low, Medium, dan High." \
    " Klik legenda di kanan untuk menyembunyikan atau menampilkan kategori tertentu.")
    with st.expander("Lihat Insight"):
        st.markdown(
        """<div style='text-align: justify'>
        Berdasarkan distribusi kategori, data memiliki komposisi yang cukup seimbang pada fitur gender dan academic_year. 
        Jumlah mahasiswa Female dan Male hampir sama, yaitu sekitar 480 ribu dan 479 ribu data, sedangkan kategori Other 
        berjumlah sekitar 40 ribu data. Pada academic_year, jumlah data tiap tingkat juga relatif seimbang, yaitu sekitar 
        249–250 ribu data. Hal ini menunjukkan bahwa dataset cukup representatif untuk melihat pola burnout berdasarkan karakteristik mahasiswa.</div>
        """, unsafe_allow_html=True)
    # Menampilkan rata - rata skor burnout berdasarkan tahun akademik
    st.subheader("Skor Burnout berdasarkan Tahun Akademik Mahasiswa")
    visualisasi_burnout_academic_year(df)
    with st.expander("Lihat Insight"):
        st.markdown(
        """<div style='text-align: justify'>
        Berdasarkan visualisasi, rata-rata burnout_score pada setiap tingkat academic_year terlihat sangat mirip. Academic year 1 dan 4 memiliki rata-rata burnout score sekitar 1,78, sedangkan academic year 2 dan 3 sedikit lebih tinggi, yaitu sekitar 1,79.
        Perbedaan nilai antar academic year sangat kecil, sehingga tingkat tahun akademik belum menunjukkan perbedaan burnout score yang signifikan secara deskriptif. Artinya, mahasiswa dari tahun akademik 1 sampai 4 memiliki kecenderungan burnout score yang relatif serupa dalam dataset ini.
        Hasil ini menunjukkan bahwa academic_year saja belum cukup kuat untuk dijadikan indikator utama dalam monitoring risiko burnout. Oleh karena itu, sistem perlu mempertimbangkan faktor lain yang lebih berkaitan dengan burnout, seperti stress_level, exam_pressure, sleep_hours, physical_activity, dan social_support.
        </div>""", unsafe_allow_html=True)
        
    # Menampilkan faktor harian yang berpengaruh paling kuat terhadap skor burnout
    st.subheader("Hubungan Faktor Harian dengan Skor Burnout Mahasiswa")
    visualisasi_daily_features_to_burnout(df)
    with st.expander("Lihat Insight"):
        st.markdown(
        """<div style='text-align: justify'>
        Berdasarkan visualisasi korelasi, faktor harian yang memiliki hubungan positif paling kuat dengan burnout_score adalah stress_level, diikuti oleh anxiety_score, depression_score, exam_pressure, study_hours_per_day, dan financial_stress. Hal ini menunjukkan bahwa semakin tinggi tingkat stres, kecemasan, depresi, tekanan ujian, durasi belajar, dan tekanan finansial, maka burnout score mahasiswa cenderung meningkat.
        Faktor seperti sleep_hours, social_support, dan physical_activity memiliki hubungan negatif dengan burnout_score. Artinya, durasi tidur yang lebih baik, dukungan sosial yang lebih tinggi, dan aktivitas fisik yang lebih baik cenderung berkaitan dengan burnout score yang lebih rendah.
        Hasil ini menunjukkan bahwa indikator psikologis, tekanan akademik, pola istirahat, dukungan sosial, dan aktivitas fisik merupakan faktor penting yang perlu dipertimbangkan dalam sistem monitoring risiko burnout. Namun, hubungan ini bersifat korelasi sehingga tidak dapat langsung disimpulkan sebagai hubungan sebab-akibat.
        </div>""", unsafe_allow_html=True)
    # Menampilkan profil kondisi harian berdasarkan risiko burnout
    st.subheader("Profil Kondisi Harian seperti Tingkat Stres, Tekanan Ujian, Durasi Tidur, Aktivitas Fisik, Dukungan Sosial, dan Screen Time berdasarkan Risiko Burnout")
    visualisasi_profil_kondisi_harian_risk_level(df)
    with st.expander("Lihat Insight"):
        st.markdown(
        """<div style='text-align: justify'>
        Berdasarkan visualisasi profil kondisi harian, mahasiswa pada kategori High risk memiliki rata-rata stress_level dan exam_pressure paling tinggi dibandingkan kategori Medium dan Low risk. Hal ini menunjukkan bahwa mahasiswa dengan tingkat risiko burnout lebih tinggi cenderung memiliki tekanan psikologis dan tekanan akademik yang lebih besar.
        Sebaliknya, kelompok High risk memiliki rata-rata sleep_hours, physical_activity, dan social_support yang lebih rendah dibandingkan kelompok Low risk. Pola ini menunjukkan bahwa mahasiswa dengan risiko burnout lebih tinggi cenderung memiliki durasi tidur yang lebih rendah, aktivitas fisik yang lebih rendah, dan dukungan sosial yang lebih rendah.
        Rata-rata screen_time terlihat relatif mirip pada semua kategori risk level, sehingga pada data ini screen time tidak menunjukkan perbedaan yang terlalu menonjol antar tingkat risiko. Dengan demikian, indikator seperti stres, tekanan ujian, durasi tidur, aktivitas fisik, dan dukungan sosial terlihat lebih relevan untuk digunakan dalam monitoring risiko burnout mahasiswa.
        </div>""", unsafe_allow_html=True)
    # Menampilkan hubungan burnout score, mental health index, dan dropout risk
    st.subheader("Hubungan Skor Burnout, Mental Health Index, dan Risiko Dropout")
    visualisasi_hubungan_target_utama(df)
    with st.expander("Lihat Insight"):
        st.markdown(
        """
        Berdasarkan heatmap korelasi, burnout_score memiliki hubungan positif dengan dropout_risk, yaitu sekitar 0,69. Artinya, semakin tinggi burnout score mahasiswa, risiko dropout cenderung ikut meningkat.
        burnout_score memiliki hubungan negatif yang kuat dengan mental_health_index, yaitu sekitar -0,80. Hal ini menunjukkan bahwa semakin tinggi burnout score, indeks kesehatan mental mahasiswa cenderung semakin rendah.
        Selain itu, mental_health_index juga memiliki hubungan negatif dengan dropout_risk, yaitu sekitar -0,63. Pola ini mendukung tujuan sistem sebagai alat bantu monitoring dan deteksi dini risiko burnout mahasiswa. Namun, hasil ini tetap perlu dipahami sebagai hubungan statistik, bukan sebagai diagnosis medis atau psikologis.
         </div>""", unsafe_allow_html=True)
    # Menampilkan kesimpulan
    st.subheader("Kesimpulan")
    st.markdown(
        """
        - Visualisasi distribusi risiko burnout menunjukkan bahwa mayoritas mahasiswa berada pada kategori risiko rendah, tetapi kelompok risiko sedang dan risiko tinggi tetap perlu dipantau karena menunjukkan indikasi burnout yang lebih tinggi.
        - Rata-rata skor burnout pada setiap tahun akademik terlihat relatif mirip, sehingga tingkat tahun akademik saja belum cukup kuat untuk menjadi indikator utama dalam pemantauan risiko burnout mahasiswa.
        - Faktor yang paling berkaitan positif dengan skor burnout adalah tingkat stres, skor kecemasan, skor depresi, tekanan ujian, jam belajar per hari, dan stres finansial. Sementara itu, faktor yang berkaitan negatif adalah jam tidur, dukungan sosial, dan aktivitas fisik.
        - Mahasiswa pada kategori risiko burnout tinggi cenderung memiliki tingkat stres dan tekanan ujian yang lebih tinggi, serta jam tidur, aktivitas fisik, dan dukungan sosial yang lebih rendah dibandingkan mahasiswa pada kategori risiko burnout rendah.
        - Skor burnout memiliki hubungan positif dengan risiko putus studi (dropout) dan hubungan negatif dengan indeks kesehatan mental. Hasil ini mendukung pengembangan sistem sebagai alat bantu pemantauan dan deteksi dini risiko burnout mahasiswa, bukan sebagai alat diagnosis medis atau psikologis.
        """
            )
# Halaman prediksin risiko burnout
elif st.session_state.page == "📝 Prediksi Risiko Burnout":
    st.title("Prediksi Risiko Burnout menggunakan Bantuan AI")
  
    def warna_risk_level(label):
        if label == "Rendah":
            return "#2196F3"   # Biru
        elif label == "Sedang":
            return "#FFC107"   # Kuning
        elif label == "Tinggi":
            return "#F44336"   # Merah
        else:
            return "#9E9E9E"
        
    def warna_mental_health(label):
        if label == "Buruk":
            return "#F44336"   # Merah
        elif label == "Sedang":
            return "#FFC107"   # Kuning
        elif label == "Baik":
            return "#2196F3"   # Biru
        else:
            return "#9E9E9E"
    
    feature_cols = [
        "stress_level",
        "anxiety_score",
        "depression_score",
        "exam_pressure",
        "sleep_hours",
        "study_hours_per_day",
        "financial_stress",
        "family_expectation",
        "social_support",
        "physical_activity"
    ]

    with st.form("form_prediksi"):
        stress_level = st.slider("Tingkat Stres", 0.0, 10.0, 5.0)
        anxiety_score = st.slider("Skor Kecemasan", 0.0, 10.0, 5.0)
        depression_score = st.slider("Skor Depresi", 0.0, 10.0, 5.0)
        exam_pressure = st.slider("Tekanan Ujian", 1.0, 10.0, 5.0)
        sleep_hours = st.slider("Durasi Tidur per Hari", 0.0, 24.0, 7.0)
        study_hours_per_day = st.slider("Durasi Belajar per Hari", 0.0, 24.0, 4.0)
        financial_stress = st.slider("Tekanan Finansial", 0.0, 10.0, 5.0)
        family_expectation = st.slider("Ekspektasi Keluarga", 0.0, 10.0, 5.0)
        social_support = st.slider("Dukungan Sosial", 0.0, 10.0, 5.0)
        physical_activity = st.slider("Aktivitas Fisik per Minggu", 0.0, 24.0, 3.0)

        submitted = st.form_submit_button("Prediksi")
    
    if submitted:
        input_data = pd.DataFrame([{
            "stress_level": stress_level,
            "anxiety_score": anxiety_score,
            "depression_score": depression_score,
            "exam_pressure": exam_pressure,
            "sleep_hours": sleep_hours,
            "study_hours_per_day": study_hours_per_day,
            "financial_stress": financial_stress,
            "family_expectation": family_expectation,
            "social_support": social_support,
            "physical_activity": physical_activity
        }])
        
        input_scaled = scaler.transform(input_data[feature_cols])
        burnout_proba = burnout_model(input_scaled, training=False).numpy()[0]
        mental_health_proba = mental_health_model(input_scaled, training=False).numpy()[0]
        burnout_class = int(np.argmax(burnout_proba))
        mental_health_class = int(np.argmax(mental_health_proba))

        burnout_mapping = {
            0: "Rendah",
            1: "Sedang",
            2: "Tinggi"
        }

        mental_health_mapping = {
            0: "Buruk",
            1: "Sedang",
            2: "Baik"
        }

        pred_burnout = burnout_mapping[burnout_class]
        pred_mental_health = mental_health_mapping[mental_health_class]

        rekomendasi_burnout = {
        "Rendah": {
            "warna": "#2196F3",
            "judul": "Risiko burnout rendah",
            "rekomendasi": [
                "Pertahankan pola tidur, aktivitas fisik, dan ritme belajar yang sudah cukup stabil.",
                "Tetap lakukan pemantauan kondisi harian agar stres tidak meningkat tanpa disadari.",
                "Jaga dukungan sosial dengan tetap berkomunikasi dengan teman, keluarga, atau lingkungan kampus."
            ]
        },
        "Sedang": {
            "warna": "#FFC107",
            "judul": "Risiko burnout sedang",
            "rekomendasi": [
                "Kurangi beban belajar yang terlalu padat dengan membuat jadwal prioritas harian.",
                "Perbaiki kualitas tidur dan batasi aktivitas yang dapat memperburuk kelelahan.",
                "Cari dukungan dari teman, keluarga, dosen, atau mentor ketika tekanan akademik mulai meningkat."
            ]
        },
        "Tinggi": {
            "warna": "#F44336",
            "judul": "Risiko burnout tinggi",
            "rekomendasi": [
                "Segera kurangi aktivitas yang tidak mendesak dan fokus pada kebutuhan dasar seperti tidur, makan, dan istirahat.",
                "Bicarakan kondisi yang dirasakan kepada pihak yang dipercaya, seperti keluarga, dosen wali, mentor, atau layanan konseling kampus.",
                "Susun ulang target harian menjadi lebih realistis agar tekanan akademik tidak semakin meningkat."
            ]
        }
    }
        rekomendasi_mental_health = {
        "Buruk": {
            "warna": "#F44336",
            "judul": "Kondisi kesehatan mental perlu perhatian",
            "rekomendasi": [
                "Luangkan waktu untuk istirahat dan kurangi beban aktivitas yang tidak mendesak.",
                "Ceritakan kondisi yang dirasakan kepada orang yang dipercaya, seperti keluarga, teman dekat, mentor, dosen wali, atau layanan konseling kampus.",
                "Jaga kebutuhan dasar seperti tidur cukup, makan teratur, dan mengurangi paparan aktivitas digital yang melelahkan."
            ]
        },
        "Sedang": {
            "warna": "#FFC107",
            "judul": "Kondisi kesehatan mental perlu dipantau",
            "rekomendasi": [
                "Pertahankan rutinitas harian yang seimbang antara belajar, istirahat, dan aktivitas sosial.",
                "Perhatikan tanda-tanda kelelahan, stres, atau perubahan suasana hati agar tidak berkembang menjadi lebih berat.",
                "Gunakan strategi sederhana seperti membuat prioritas tugas, menjaga tidur, dan meluangkan waktu untuk aktivitas yang menyenangkan."
            ]
        },
        "Baik": {
            "warna": "#2196F3",
            "judul": "Kondisi kesehatan mental relatif baik",
            "rekomendasi": [
                "Pertahankan kebiasaan positif seperti tidur cukup, aktivitas fisik, dan komunikasi sosial yang sehat.",
                "Tetap lakukan evaluasi diri secara berkala agar kondisi mental tetap terjaga.",
                "Bantu menjaga lingkungan belajar yang suportif, baik untuk diri sendiri maupun teman sekitar."
            ]
        }
    }
        st.subheader("Hasil Prediksi")

        warna_burnout = warna_risk_level(pred_burnout)
        warna_mh = warna_mental_health(pred_mental_health)

        hasil_col1, hasil_col2 = st.columns(2)
        
        with hasil_col1:
            st.markdown(
                    f"""
                    <div style="
                        border: 1.5px solid {warna_burnout};
                        border-left: 6px solid {warna_burnout};
                        border-radius: 10px;
                        padding: 16px;
                        background-color: rgba(255, 255, 255, 0.03);
                    ">
                        <p style="margin:0; font-size:14px; color:#AFAFAF;">
                            Prediksi Risk Level Burnout
                        </p>
                        <h2 style="margin:6px 0 0 0; color:{warna_burnout};">
                            {pred_burnout}
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        with hasil_col2:
             st.markdown(
                    f"""
                    <div style="
                        border: 1.5px solid {warna_mh};
                        border-left: 6px solid {warna_mh};
                        border-radius: 10px;
                        padding: 16px;
                        background-color: rgba(255, 255, 255, 0.03);
                    ">
                        <p style="margin:0; font-size:14px; color:#AFAFAF;">
                            Prediksi Kategori Kesehatan Mental
                        </p>
                        <h2 style="margin:6px 0 0 0; color:{warna_mh};">
                            {pred_mental_health}
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        burnout_df = pd.DataFrame({
            "Kelas": ["Low", "Medium", "High"],
            "Probabilitas": burnout_proba
        })

        mental_health_df = pd.DataFrame({
            "Kelas": ["Buruk", "Sedang", "Baik"],
            "Probabilitas": mental_health_proba
        })

        # Ubah probabilitas menjadi persentase
        burnout_df["Persentase"] = burnout_df["Probabilitas"] * 100
        mental_health_df["Persentase"] = mental_health_df["Probabilitas"] * 100

        # Buat label persentase
        burnout_df["Label"] = burnout_df["Persentase"].apply(lambda x: f"{x:.1f}%")
        mental_health_df["Label"] = mental_health_df["Persentase"].apply(lambda x: f"{x:.1f}%")

        fig_burnout = px.bar(
            burnout_df,
            x="Kelas",
            y="Persentase",
            text="Label",
            title="Probabilitas Risiko Burnout"
        )

        fig_burnout.update_layout(
            xaxis_title="Kelas",
            yaxis_title="Persentase (%)",
            height=400,
            yaxis=dict(
                ticksuffix="%",
                range=[0, burnout_df["Persentase"].max() * 1.2])
        )

        fig_burnout.update_traces(textposition="outside")

        st.plotly_chart(fig_burnout, use_container_width=True)

        fig_mental = px.bar(
            mental_health_df,
            x="Kelas",
            y="Persentase",
            text="Label",
            title="Probabilitas Kesehatan Mental"
        )

        fig_mental.update_layout(
            xaxis_title="Kelas",
            yaxis_title="Persentase",
            height=400
        )

        fig_mental.update_traces(textposition="outside")

        st.plotly_chart(fig_mental, use_container_width=True)


        data_rekomendasi = rekomendasi_burnout[pred_burnout]
        data_rekomendasi_mh = rekomendasi_mental_health.get(pred_mental_health)

        st.markdown(
            f"""
            <div style="
                border-left: 6px solid {data_rekomendasi['warna']};
                background-color: rgba(255, 255, 255, 0.04);
                padding: 18px 22px;
                border-radius: 10px;
                margin-top: 20px;
                margin-bottom: 20px;
            ">
                <h4 style="margin-top: 0; color: {data_rekomendasi['warna']};">
                    Rekomendasi: {data_rekomendasi['judul']}
                </h4>
                <ol style="font-size: 16px; line-height: 1.7; margin-bottom: 0;">
                    <li>{data_rekomendasi['rekomendasi'][0]}</li>
                    <li>{data_rekomendasi['rekomendasi'][1]}</li>
                    <li>{data_rekomendasi['rekomendasi'][2]}</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                border-left: 6px solid {data_rekomendasi_mh['warna']};
                background-color: rgba(255, 255, 255, 0.04);
                padding: 18px 22px;
                border-radius: 10px;
                margin-top: 20px;
                margin-bottom: 20px;
            ">
                <h4 style="margin-top: 0; color: {data_rekomendasi_mh['warna']};">
                    Rekomendasi Kesehatan Mental: {data_rekomendasi_mh['judul']}
                </h4>
                <ol style="font-size: 16px; line-height: 1.7; margin-bottom: 0;">
                    <li>{data_rekomendasi_mh['rekomendasi'][0]}</li>
                    <li>{data_rekomendasi_mh['rekomendasi'][1]}</li>
                    <li>{data_rekomendasi_mh['rekomendasi'][2]}</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.error(
        "Catatan: Rekomendasi ini bersifat umum dan digunakan untuk simulasi aplikasi. "
        "Hasil prediksi tidak dapat menggantikan penilaian profesional."
        )
        st.subheader("Data Input Pengguna")
        st.dataframe(input_data, use_container_width=True)