from flask import Flask, render_template, request  # 确保导入 render_template 和 request
from flask_sqlalchemy import SQLAlchemy
import os
from collections import defaultdict

app = Flask(__name__)

# 从环境变量中读取数据库连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError(
        "请设置环境变量 DATABASE_URI，例如：\n"
        "export DATABASE_URI='mysql+pymysql://root:your_password@localhost/VirusFactor?charset=utf8mb4'"
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/test-db')
def test_db():
    try:
        db.engine.connect()
        return "Database connection successful", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500

# 定义数据库模型
class Pathogen(db.Model):
    __tablename__ = 'Pathogen'
    Pathogen_id = db.Column(db.Integer, primary_key=True)
    PathogenName = db.Column(db.String(255), nullable=False)
    SequenceStrain = db.Column(db.String(255))

class Gene(db.Model):
    __tablename__ = 'Gene'
    Gene_id = db.Column(db.Integer, primary_key=True)
    GeneName = db.Column(db.String(255), nullable=False)
    ncbiGeneID = db.Column(db.String(255))
    ncbiNucleotideGI = db.Column(db.String(255))
    LocusTag = db.Column(db.String(255))
    GenbankAccession = db.Column(db.String(255))
    PMID = db.Column(db.String(255))
    Pathogen_id = db.Column(db.Integer, db.ForeignKey('Pathogen.Pathogen_id'))
    Protein_id = db.Column(db.Integer, db.ForeignKey('Protein.Protein_id'))

class Protein(db.Model):
    __tablename__ = 'Protein'
    Protein_id = db.Column(db.Integer, primary_key=True)
    ncbiProteinGI = db.Column(db.String(255))
    ProteinAccession = db.Column(db.String(255))
    ProteinName = db.Column(db.String(255))
    MolecularRole = db.Column(db.Text)
    COG = db.Column(db.String(255))
    PMID = db.Column(db.String(255))
    Pathogen_id = db.Column(db.Integer, db.ForeignKey('Pathogen.Pathogen_id'))

# 首页
@app.route('/')
def index():
    pathogen_names = [
        "porcine respiratory coronavirus",
        "Acinetobacter baumannii",
        "Actinobacillus pleuropneumoniae",
        "Aeromonas hydrophila",
        "Aeromonas salmonicida",
        "African swine fever virus",
        "Aspergillus fumigatus",
        "Autographa californica nuclear polyhedrosis virus",
        "Babesia bovis",
        "Bacillus anthracis",
        "Bartonella sp.",
        "Bombyx mori nucleopolyhedrovirus",
        "Bordetella avium",
        "Bordetella bronchiseptica",
        "Bordetella pertussis",
        "Borrelia burgdorferi",
        "Bovine herpesvirus 1",
        "Bovine herpesvirus 5",
        "Bovine respiratory syncytial virus",
        "Brucella spp.",
        "Burkholderia mallei",
        "Burkholderia pseudomallei",
        "Campylobacter jejuni",
        "Candida albicans",
        "Candida glabrata",
        "Chicken Anemia Virus",
        "Chlamydia trachomatis",
        "Chlamydophila pneumoniae",
        "Classical swine fever virus",
        "Clostridium botulinum",
        "Clostridium difficile",
        "Clostridium perfringens",
        "Clostridium tetani",
        "Coccidioides sp.",
        "Corynebacterium diphtheriae",
        "Coxiella burnetii",
        "Cryptococcus neoformans",
        "Cryptosporidium parvum",
        "Ebola virus",
        "Ectromelia virus",
        "Edwardsiella tarda",
        "encephalomyocarditis virus",
        "Entamoeba histolytica",
        "Enterococcus spp.",
        "Equid herpesvirus",
        "Escherichia coli",
        "Fasciola hepatica",
        "Feline herpesvirus 1",
        "Feline immunodeficiency virus",
        "Feline infectious peritonitis virus",
        "Francisella tularensis",
        "frog virus 3",
        "Gallid herpesvirus 1",
        "Haemophilus influenzae",
        "Hantavirus",
        "Helicobacter pylori",
        "Hepatitis B virus",
        "Herpes simplex virus type 1",
        "Histoplasma capsulatum",
        "Human immunodeficiency virus",
        "Human metapneumovirus",
        "Human parainfluenza virus type 3",
        "Human Respiratory Syncytial Virus",
        "Infectious Bronchitis Virus",
        "Infectious Bursal Disease Virus",
        "Infectious hematopoietic necrosis virus",
        "infectious laryngotracheitis virus",
        "Influenza virus",
        "La Crosse virus",
        "Legionella pneumophila",
        "Leishmania amazonensis",
        "Leishmania donovani",
        "Leishmania infantum",
        "Leishmania major",
        "Leishmania mexicana",
        "Leptospira sp.",
        "Listeria monocytogenes",
        "Mannheimia haemolytica",
        "Marek's disease virus",
        "Measles virus",
        "MERS coronavirus",
        "murine cytomegalovirus",
        "Mycobacterium avium",
        "Mycobacterium tuberculosis",
        "Mycoplasma gallisepticum",
        "Myxoma virus",
        "Neisseria meningitidis",
        "Newcastle disease virus",
        "Nipah virus",
        "Orf Virus",
        "Pasteurella multocida",
        "Plasmodium spp.",
        "Pneumonia virus of mice",
        "Porcine circovirus 2",
        "Porcine respiratory and reproductive syndrome virus",
        "Pseudomonas aeruginosa",
        "Pseudorabies virus",
        "Rabbit fibroma virus",
        "Rabies virus",
        "Rickettsia sp.",
        "Rift valley fever virus",
        "Ross River virus",
        "Rotavirus",
        "Saccharomyces cerevisiae",
        "Salmonella sp.",
        "SARS-related coronavirus",
        "Schistosoma mansoni",
        "Sheeppox virus",
        "Shigella",
        "Simian immunodeficiency virus",
        "Sindbis virus",
        "Staphylococcus aureus",
        "Streptococcus agalactiae",
        "Streptococcus equi",
        "Streptococcus pneumoniae",
        "Streptococcus pyogenes",
        "Tick-borne Encephalitis Virus",
        "Toxoplasma gondii",
        "Trypanosoma brucei",
        "Trypanosoma cruzi",
        "Vaccinia virus",
        "VEE Virus",
        "Vibrio cholerae",
        "Wangiella dermatitidis",
        "West Nile virus",
        "Western equine encephalomyelitis virus",
        "Yellow fever virus",
        "Yersinia enterocolitica",
        "Yersinia pestis",
        "Yersinia pseudotuberculosis",
        "Yersinia ruckeri"
        ]
    # 按首字母顺序排序
    pathogen_names_sorted = sorted(pathogen_names, key=lambda x: x.lower())
    return render_template('index.html', pathogen_names=pathogen_names_sorted)

# Virulence Factors of Pathogen
@app.route('/search_p2', methods=['POST'])
def search_p2():
    pathogen_name = request.form['pathogen_name']
    results = db.session.query(Pathogen, Gene).join(Gene, Pathogen.Pathogen_id == Gene.Pathogen_id)\
        .filter(Pathogen.PathogenName == pathogen_name).all()
    return render_template('p2_result.html', results=results, pathogen_name=pathogen_name)

# Gene-Function Annotation
@app.route('/search_p3', methods=['POST'])
def search_p3():
    gene_name = request.form['gene_name']
    results = db.session.query(Pathogen, Gene, Protein)\
        .join(Gene, Pathogen.Pathogen_id == Gene.Pathogen_id)\
        .join(Protein, Gene.Protein_id == Protein.Protein_id)\
        .filter(Gene.GeneName == gene_name).all()
    return render_template('p3_result.html', results=results, gene_name=gene_name)

# Functional Annotation of Pathogen
@app.route('/search_p4', methods=['POST'])
def search_p4():
    pathogen_name = request.form['pathogen_name']
    results = db.session.query(Pathogen, Protein).join(Protein, Pathogen.Pathogen_id == Protein.Pathogen_id)\
        .filter(Pathogen.PathogenName == pathogen_name).all()

    # 统计 COG 字段中的注释频率
    cog_stats = defaultdict(int)
    total = 0
    for _, protein in results:
        if protein.COG and 'under ' in protein.COG:
            cog_char = protein.COG.split('under ')[-1].strip()[0]  # 获取 `under` 后的第一个字符
            cog_stats[cog_char] += 1
            total += 1
        elif not protein.COG:
            cog_stats['Unknown'] += 1
            total += 1

    cog_distribution = {char: count for char, count in cog_stats.items()}
    total_proteins = total

    return render_template(
        'p4_result.html',
        results=results,
        pathogen_name=pathogen_name,
        cog_distribution=cog_distribution,
        total_proteins=total_proteins
    )

if __name__ == '__main__':
    app.run(debug=True)
