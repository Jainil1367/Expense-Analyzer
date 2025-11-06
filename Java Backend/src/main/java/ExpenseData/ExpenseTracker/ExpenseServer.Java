package com.expensetracker;

import static spark.Spark.*;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.util.*;

public class ExpenseServer {
    static Gson gson = new GsonBuilder().setPrettyPrinting().create();
    static String CSV_FILE = "../shared-data/expenses.csv";
    static String PROFILE_FILE = "../shared-data/user-profile.json";

    public static void main(String[] args) {
        port(4567);
        
        initFiles();

        // CORS Configuration
        before((req, res) -> {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
            res.header("Access-Control-Allow-Headers", "Content-Type");
        });

        options("/*", (req, res) -> "OK");

        // User Profile Endpoints
        post("/profile", (req, res) -> {
            try {
                UserProfile profile = gson.fromJson(req.body(), UserProfile.class);
                saveProfile(profile);
                res.type("application/json");
                return gson.toJson(Map.of("success", true, "message", "Profile saved successfully"));
            } catch (Exception e) {
                res.status(400);
                res.type("application/json");
                return gson.toJson(Map.of("success", false, "message", e.getMessage()));
            }
        });

        get("/profile", (req, res) -> {
            res.type("application/json");
            UserProfile profile = loadProfile();
            return gson.toJson(profile);
        });

        // Expense Endpoints
        post("/add", (req, res) -> {
            try {
                Expense e = gson.fromJson(req.body(), Expense.class);
                if (e.id == 0) {
                    e.id = System.currentTimeMillis();
                }
                saveExpense(e);
                res.type("application/json");
                return gson.toJson(Map.of("success", true, "message", "Expense added", "expense", e));
            } catch (Exception e) {
                res.status(400);
                res.type("application/json");
                return gson.toJson(Map.of("success", false, "message", e.getMessage()));
            }
        });

        get("/expenses", (req, res) -> {
            res.type("application/json");
            return gson.toJson(loadExpenses());
        });

        delete("/expense/:id", (req, res) -> {
            try {
                long id = Long.parseLong(req.params(":id"));
                deleteExpense(id);
                res.type("application/json");
                return gson.toJson(Map.of("success", true, "message", "Expense deleted"));
            } catch (Exception e) {
                res.status(400);
                res.type("application/json");
                return gson.toJson(Map.of("success", false, "message", e.getMessage()));
            }
        });

        get("/stats", (req, res) -> {
            res.type("application/json");
            List<Expense> expenses = loadExpenses();
            
            double total = expenses.stream().mapToDouble(e -> e.amount).sum();
            double average = expenses.isEmpty() ? 0 : total / expenses.size();
            long categories = expenses.stream().map(e -> e.category).distinct().count();
            
            Map<String, Object> stats = new HashMap<>();
            stats.put("total", total);
            stats.put("count", expenses.size());
            stats.put("average", average);
            stats.put("categories", categories);
            
            return gson.toJson(stats);
        });

        System.out.println("\n" + "=".repeat(60));
        System.out.println("✅ Expense Tracker API Server Started!");
        System.out.println("=".repeat(60));
        System.out.println("🌐 Server: http://localhost:4567");
        System.out.println("📊 Ready to accept requests");
        System.out.println("=".repeat(60) + "\n");
    }

    static void initFiles() {
        try {
            File dataDir = new File("../shared-data");
            if (!dataDir.exists()) {
                dataDir.mkdirs();
            }
            
            File csvFile = new File(CSV_FILE);
            if (!csvFile.exists()) {
                try (PrintWriter pw = new PrintWriter(new FileWriter(CSV_FILE))) {
                    pw.println("id,date,category,amount");
                }
                System.out.println("✅ Created: expenses.csv");
            }
            
            File profileFile = new File(PROFILE_FILE);
            if (!profileFile.exists()) {
                UserProfile defaultProfile = new UserProfile(0, false);
                try (FileWriter fw = new FileWriter(PROFILE_FILE)) {
                    gson.toJson(defaultProfile, fw);
                }
                System.out.println("✅ Created: user-profile.json");
            }
        } catch (IOException e) {
            System.err.println("❌ Error: " + e.getMessage());
        }
    }

    static void saveProfile(UserProfile profile) throws IOException {
        try (FileWriter fw = new FileWriter(PROFILE_FILE)) {
            gson.toJson(profile, fw);
        }
        System.out.println("💾 Profile saved: $" + profile.salary);
    }

    static UserProfile loadProfile() {
        try (FileReader fr = new FileReader(PROFILE_FILE)) {
            UserProfile profile = gson.fromJson(fr, UserProfile.class);
            return profile != null ? profile : new UserProfile(0, false);
        } catch (IOException e) {
            return new UserProfile(0, false);
        }
    }

    static void saveExpense(Expense e) throws IOException {
        try (PrintWriter pw = new PrintWriter(new FileWriter(CSV_FILE, true))) {
            pw.println(e.id + "," + e.date + "," + e.category + "," + e.amount);
        }
        System.out.println("➕ Added: " + e.category + " $" + e.amount);
    }

    static List<Expense> loadExpenses() {
        List<Expense> list = new ArrayList<>();
        File file = new File(CSV_FILE);
        if (!file.exists()) return list;

        try (Scanner sc = new Scanner(file)) {
            if (sc.hasNextLine()) sc.nextLine();
            
            while (sc.hasNextLine()) {
                String line = sc.nextLine();
                if (line.trim().isEmpty()) continue;
                
                try {
                    String[] data = line.split(",");
                    if (data.length == 4) {
                        long id = Long.parseLong(data[0].trim());
                        String date = data[1].trim();
                        String category = data[2].trim();
                        double amount = Double.parseDouble(data[3].trim());
                        list.add(new Expense(id, date, category, amount));
                    }
                } catch (Exception e) {
                    System.err.println("⚠️  Skipping line: " + line);
                }
            }
        } catch (IOException e) {
            System.err.println("❌ Error: " + e.getMessage());
        }
        return list;
    }

    static void deleteExpense(long id) throws IOException {
        List<Expense> expenses = loadExpenses();
        expenses.removeIf(e -> e.id == id);
        
        try (PrintWriter pw = new PrintWriter(new FileWriter(CSV_FILE))) {
            pw.println("id,date,category,amount");
            for (Expense e : expenses) {
                pw.println(e.id + "," + e.date + "," + e.category + "," + e.amount);
            }
        }
        System.out.println("🗑️  Deleted: ID=" + id);
    }
}