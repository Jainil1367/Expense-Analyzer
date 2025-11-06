package com.expensetracker;

public class Expense {
    public long id;
    public String date;
    public String category;
    public double amount;

    public Expense(long id, String date, String category, double amount) {
        this.id = id;
        this.date = date;
        this.category = category;
        this.amount = amount;
    }
    
    public Expense(String date, String category, double amount) {
        this.id = System.currentTimeMillis();
        this.date = date;
        this.category = category;
        this.amount = amount;
    }
}