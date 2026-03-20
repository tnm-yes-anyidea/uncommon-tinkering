import matplotlib.pyplot as plt
import pandas as pd

data = {
    "Country": [
        "USA",
        "UAE",
        "Canada",
        "Malaysia",
        "Saudi Arabia",
        "Myanmar",
        "Sri Lanka",
        "South Africa",
        "United Kingdom",
        "Kuwait",
        "Australia",
        "Mauritius",
        "Oman",
        "Qatar",
        "Trinidad & Tobago",
        "Singapore",
        "Bahrain",
        "Guyana",
        "Fiji",
        "France (inc. Reunion)",
        "Germany",
        "Italy",
        "Suriname",
        "Netherlands",
        "Indonesia",
        "Israel",
        "Kenya",
        "Jamaica",
        "Ireland",
        "Bhutan",
        "Guadeloupe",
        "Spain",
        "New Zealand",
        "Japan",
        "Tanzania",
        "Zambia",
        "Belgium",
        "Norway",
        "Maldives",
        "Switzerland",
        "Portugal",
        "Philippines",
        "Sweden",
        "Finland",
        "Denmark",
        "Congo (DRC)",
        "Saint Lucia",
        "Malta",
        "Iraq",
        "Jordan",
    ],
    "NRIs": [
        1920000,
        3890000,
        1751610,
        185000,
        2750000,
        2660,
        7500,
        74057,
        369000,
        1010000,
        350000,
        10500,
        710000,
        705000,
        11500,
        160000,
        323908,
        1500,
        2283,
        29000,
        208000,
        167333,
        500,
        15000,
        14817,
        20000,
        20000,
        5000,
        30000,
        60000,
        180,
        45000,
        80000,
        46262,
        5000,
        5000,
        17438,
        16890,
        27065,
        17059,
        21000,
        15000,
        22000,
        8245,
        17460,
        15000,
        550,
        18000,
        17100,
        16897,
    ],
    "PIOs": [
        3770000,
        10000,
        1859680,
        2755000,
        0,
        2000000,
        1602500,
        1315943,
        971000,
        2356,
        626000,
        884000,
        2000,
        0,
        528500,
        300000,
        3899,
        320000,
        313798,
        271159,
        52864,
        39170,
        179500,
        135000,
        120000,
        85000,
        60000,
        68000,
        31386,
        0,
        57000,
        10000,
        160000,
        1548,
        30000,
        25000,
        11396,
        10955,
        135,
        8996,
        4000,
        10000,
        3000,
        13114,
        3187,
        5000,
        18600,
        250,
        4,
        153,
    ],
    "Total_Diaspora": [
        5690000,
        3900000,
        3611290,
        2940000,
        2750000,
        2002660,
        1610000,
        1390000,
        1340000,
        1012356,
        976000,
        894500,
        712000,
        705000,
        540000,
        460000,
        327807,
        321500,
        316081,
        300159,
        260864,
        206503,
        180000,
        150000,
        134817,
        105000,
        80000,
        73000,
        61386,
        60000,
        57180,
        55000,
        240000,
        47810,
        35000,
        30000,
        28834,
        27845,
        27200,
        26055,
        25000,
        25000,
        25000,
        21359,
        20647,
        20000,
        19150,
        18250,
        17104,
        17050,
    ],
    "Host_Country_Population": [
        347694430,
        11305020,
        40118870,
        36116760,
        34841920,
        54421240,
        23213060,
        64978480,
        69545810,
        4500000,
        27084160,
        1300000,
        5671458,
        2800000,
        1540000,
        5905748,
        1500000,
        810000,
        940000,
        66655520,
        84192410,
        58865750,
        630000,
        18275460,
        285871330,
        9624280,
        58171930,
        2800000,
        5200000,
        800000,
        400000,
        47719600,
        5300000,
        122560220,
        72469700,
        22388580,
        11747220,
        5652989,
        520000,
        9007798,
        10383350,
        117030070,
        10651980,
        5621739,
        6023520,
        116253260,
        185000,
        540000,
        47699460,
        12035110,
    ],
}

df = pd.DataFrame(data)
df["%_of_Host_Pop"] = (
    df["Total_Diaspora"] / df["Host_Country_Population"] * 100).round(2)
print(df.head(50))

df.to_csv('Indian-Diaspora.csv', index=False, sep='\t', encoding='utf-8')

# Create a figure with 2x2 subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))
fig.suptitle('Global Indian Diaspora Analysis',
             fontsize=24, fontweight='bold', y=1.02)

# 1. Bar Chart: Top 10 Countries by Total Diaspora
# Get top 10 using pandas (already in your code)
top_10 = df.nlargest(10, 'Total_Diaspora').sort_values(
    'Total_Diaspora', ascending=True)
ax1 = axes[0, 0]

# Generate colors without numpy using a simple list comprehension
cmap = plt.get_cmap('viridis')
colors = [cmap(i/10) for i in range(10)]

bars = ax1.barh(top_10['Country'], top_10['Total_Diaspora'], color=colors)
ax1.set_title('Top 10 Countries by Total Diaspora',
              fontsize=16, fontweight='bold')
ax1.set_xlabel('Total Diaspora', fontsize=12)

# Formatting X-axis with commas
ax1.xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: format(int(x), ',')))

for bar in bars:
    width = bar.get_width()
    ax1.text(width, bar.get_y() + bar.get_height() / 2,
             f' {width/1e6:.1f}M', va='center', fontweight='bold')

# 2. Scatter Plot: Host Population vs Diaspora (Log Scale)
ax2 = axes[0, 1]
scatter = ax2.scatter(df['Host_Country_Population'], df['Total_Diaspora'],
                      s=df['%_of_Host_Pop']*25, c=df['%_of_Host_Pop'],
                      cmap='plasma', alpha=0.7, edgecolors='w')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_title('Host Population vs Indian Diaspora Size',
              fontsize=16, fontweight='bold')
ax2.set_xlabel('Host Country Population (Log Scale)')
ax2.set_ylabel('Total Diaspora (Log Scale)')
cbar = fig.colorbar(scatter, ax=ax2)
cbar.set_label('% of Host Country Population')

# 3. Donut Chart: Global NRI vs PIO Distribution
ax3 = axes[1, 0]
total_nri = sum(data["NRIs"])
total_pio = sum(data["PIOs"])
ax3.pie([total_nri, total_pio], labels=['NRIs', 'PIOs'], colors=['#ff9999', '#66b3ff'],
        autopct='%1.1f%%', startangle=90, pctdistance=0.85, wedgeprops={'width': 0.3})
ax3.set_title('Global Diaspora Composition', fontsize=16, fontweight='bold')

# 4. Box Plot: Distribution of % Concentration
ax4 = axes[1, 1]
ax4.boxplot(df['%_of_Host_Pop'], vert=False, patch_artist=True,
            boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red'))
ax4.set_title('Density (% of Host Population) Spread',
              fontsize=16, fontweight='bold')
ax4.set_xlabel('% Concentration')

plt.tight_layout()
plt.savefig('diaspora_analysis.png', bbox_inches='tight')
plt.show()
