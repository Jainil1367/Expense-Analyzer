#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "..", "shared-data", "expenses.csv")
PROFILE_FILE = os.path.join(BASE_DIR, "..", "shared-data", "user-profile.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('dark_background')

def load_profile():
    try:
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'salary': 50000, 'setup': False}

def get_benchmark_data(salary):
    if salary < 30000:
        return {'housing': 0.38, 'food': 0.16, 'transportation': 0.18, 
                'utilities': 0.08, 'entertainment': 0.05, 'healthcare': 0.08, 'savings': 0.07}
    elif salary < 50000:
        return {'housing': 0.35, 'food': 0.14, 'transportation': 0.17,
                'utilities': 0.07, 'entertainment': 0.07, 'healthcare': 0.07, 'savings': 0.13}
    elif salary < 75000:
        return {'housing': 0.33, 'food': 0.13, 'transportation': 0.16,
                'utilities': 0.06, 'entertainment': 0.09, 'healthcare': 0.06, 'savings': 0.17}
    elif salary < 100000:
        return {'housing': 0.30, 'food': 0.12, 'transportation': 0.15,
                'utilities': 0.05, 'entertainment': 0.10, 'healthcare': 0.05, 'savings': 0.23}
    else:
        return {'housing': 0.27, 'food': 0.10, 'transportation': 0.12,
                'utilities': 0.04, 'entertainment': 0.12, 'healthcare': 0.05, 'savings': 0.30}

def create_category_chart(expenses):
    category_totals = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(14, 7))
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', 
              '#EC4899', '#06B6D4', '#F97316', '#14B8A6', '#A855F7', '#6B7280']
    
    bars = plt.bar(range(len(category_totals)), category_totals.values, 
                   color=colors[:len(category_totals)], edgecolor='white', linewidth=2)
    
    plt.xlabel('Category', fontsize=14, fontweight='bold')
    plt.ylabel('Amount ($)', fontsize=14, fontweight='bold')
    plt.title('Spending by Category', fontsize=18, fontweight='bold', pad=20)
    plt.xticks(range(len(category_totals)), category_totals.index, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/category_chart.png', dpi=150, bbox_inches='tight', 
                facecolor='#1F2937', edgecolor='none')
    plt.close()
    print("✅ Category chart created")

def create_timeline_chart(expenses):
    # Ensure date column is datetime
    if 'date' in expenses.columns:
        try:
            expenses['date'] = pd.to_datetime(expenses['date'])
        except Exception:
            pass

    timeline = expenses.groupby('date')['amount'].sum().sort_index()

    if timeline.empty:
        print("⚠️  Timeline data empty — skipping timeline chart")
        return

    plt.figure(figsize=(14, 7))
    plt.plot(timeline.index, timeline.values, marker='o', linewidth=3,
             markersize=8, color='#10B981', markerfacecolor='#10B981',
             markeredgecolor='white', markeredgewidth=2.0)

    plt.xlabel('Date', fontsize=14, fontweight='bold')
    plt.ylabel('Daily Spending ($)', fontsize=14, fontweight='bold')
    plt.title('Spending Timeline', fontsize=18, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, linestyle='--')

    # Use index values for fill_between when index is datetime
    try:
        x_vals = timeline.index
        plt.fill_between(x_vals, timeline.values, alpha=0.3, color='#10B981')
    except Exception:
        plt.fill_between(range(len(timeline)), timeline.values, alpha=0.3, color='#10B981')

    avg = timeline.mean()
    plt.axhline(y=avg, color='#F59E0B', linestyle='--', linewidth=2, label=f'Avg: ${avg:.2f}')
    plt.legend()

    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'timeline_chart.png'), dpi=150, bbox_inches='tight',
                facecolor='#1F2937', edgecolor='none')
    plt.close()
    print("✅ Timeline chart created")

def create_comparison_chart(expenses, salary):
    monthly_salary = salary / 12
    benchmark = get_benchmark_data(salary)
    
    # Map user categories to benchmark keys (lowercase)
    category_map = {
        'Housing': 'housing', 'Food': 'food', 'Dining Out': 'food',
        'Transportation': 'transportation', 'Utilities': 'utilities',
        'Phone': 'utilities', 'Entertainment': 'entertainment',
        'Shopping': 'entertainment', 'Healthcare': 'healthcare',
        'Education': 'education', 'Other': 'other'
    }

    # Ensure benchmark contains keys for education and other
    for k in ('education', 'other'):
        if k not in benchmark:
            benchmark[k] = 0.0

    user_spending = {key: 0 for key in benchmark.keys()}
    
    for _, exp in expenses.iterrows():
        mapped_cat = category_map.get(exp['category'], 'other')
        if mapped_cat in user_spending:
            user_spending[mapped_cat] += exp['amount']
    
    categories = list(benchmark.keys())
    user_pct = [(user_spending[cat] / monthly_salary * 100) if monthly_salary > 0 else 0 
                for cat in categories]
    avg_pct = [benchmark[cat] * 100 for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(16, 8))
    bars1 = ax.bar(x - width/2, user_pct, width, label='Your Spending', 
                   color='#3B82F6', edgecolor='white', linewidth=2)
    bars2 = ax.bar(x + width/2, avg_pct, width, label='National Average', 
                   color='#10B981', edgecolor='white', linewidth=2)
    
    ax.set_xlabel('Category', fontsize=14, fontweight='bold')
    ax.set_ylabel('Percentage of Income (%)', fontsize=14, fontweight='bold')
    ax.set_title('Your Spending vs National Average (BLS Data)', fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([cat.capitalize() for cat in categories], rotation=45, ha='right')
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparison_chart.png', dpi=150, bbox_inches='tight',
                facecolor='#1F2937', edgecolor='none')
    plt.close()
    print("✅ Comparison chart created")

def print_summary(expenses, salary):
    total = expenses['amount'].sum()
    monthly_salary = salary / 12
    spending_rate = (total / monthly_salary * 100) if monthly_salary > 0 else 0
    
    print("\n" + "="*70)
    print("📊 EXPENSE SUMMARY".center(70))
    print("="*70)
    print(f"💰 Annual Salary: ${salary:,.2f}")
    print(f"💵 Monthly Budget: ${monthly_salary:,.2f}")
    print("-"*70)
    print(f"📈 Total Expenses: ${total:,.2f}")
    print(f"🧮 Transactions: {len(expenses)}")
    print(f"📊 Average: ${expenses['amount'].mean():.2f}")
    print(f"📉 Spending Rate: {spending_rate:.1f}%")
    
    if spending_rate > 90:
        print("⚠️  WARNING: Spending over 90%!")
    elif spending_rate > 70:
        print("⚡ CAUTION: High spending rate")
    else:
        print("✅ Good spending control")
    
    print("-"*70)
    print("🏆 Top 5 Categories:")
    category_totals = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
    for i, (cat, amount) in enumerate(category_totals.head(5).items(), 1):
        pct = (amount / total * 100) if total > 0 else 0
        print(f"  {i}. {cat:20} ${amount:>8,.2f}  ({pct:5.1f}%)")
    print("="*70 + "\n")

def generate_recommendations(expenses, salary):
    monthly_salary = salary / 12
    total = expenses['amount'].sum()
    spending_rate = (total / monthly_salary * 100) if monthly_salary > 0 else 0
    
    print("="*70)
    print("💡 FINANCIAL RECOMMENDATIONS".center(70))
    print("="*70 + "\n")
    
    if spending_rate < 70:
        surplus = monthly_salary - total
        print(f"✅ EXCELLENT! Surplus: ${surplus:,.2f}/month\n")
        print("💰 Investment Recommendations:")
        print("  1. Build emergency fund (3-6 months expenses)")
        print("  2. Max 401(k) employer match")
        print("  3. Roth IRA ($7,000/year limit)")
        print("  4. Index funds (VTI, VOO)")
    elif spending_rate > 90:
        print("⚠️  URGENT: Review all expenses immediately")
        print("  • Cut non-essential spending")
        print("  • Consider increasing income")
    else:
        print("⚡ Optimize spending to save more")
    
    print("\n" + "="*70 + "\n")

def analyze_expenses():
    print("\n" + "🚀 "*30)
    print("EXPENSE ANALYSIS STARTING".center(60))
    print("🚀 "*30 + "\n")
    
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV not found: {CSV_FILE}")
        print("   Add expenses first!")
        return
    
    try:
        expenses = pd.read_csv(CSV_FILE)
        profile = load_profile()
        salary = profile.get('salary', 50000)
        
        if expenses.empty or len(expenses) <= 1:
            print("⚠️  No expenses found!")
            return
        
        print(f"✅ Loaded {len(expenses)} expenses")
        print(f"💰 Salary: ${salary:,.2f}/year\n")
        
        print("📊 Generating charts...")
        create_category_chart(expenses)
        create_timeline_chart(expenses)
        create_comparison_chart(expenses, salary)
        
        print_summary(expenses, salary)
        generate_recommendations(expenses, salary)
        
        print("✅ "*30)
        print("ANALYSIS COMPLETE!".center(60))
        print("✅ "*30)
        print(f"\n📁 Charts: {os.path.abspath(OUTPUT_DIR)}/\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_expenses()