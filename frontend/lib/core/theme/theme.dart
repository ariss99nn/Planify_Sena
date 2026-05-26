import 'package:flutter/material.dart';

class AppTheme {
  static const Color greenPrimary  = Color(0xFF2E7D32);
  static const Color greenLight    = Color(0xFF4CAF50);
  static const Color greenSoft     = Color(0xFFE8F5E9);
  // ✅ Color precalculado — withOpacity() no puede usarse en contexto const
  static const Color greenSoftFill = Color(0xFFF1FAF1);
  static const Color white         = Color(0xFFFFFFFF);
  static const Color textDark      = Color(0xFF1B5E20);

  static ThemeData light = ThemeData(
    useMaterial3: true,

    colorScheme: ColorScheme.fromSeed(
      seedColor: greenPrimary,
      brightness: Brightness.light,
      primary: greenPrimary,
      secondary: greenLight,
      surface: white,
      error: Colors.red,
    ),

    scaffoldBackgroundColor: greenSoft,

    appBarTheme: const AppBarTheme(
      backgroundColor: greenPrimary,
      foregroundColor: white,
      elevation: 0,
      centerTitle: true,
    ),

    inputDecorationTheme: InputDecorationTheme(
      labelStyle: const TextStyle(color: greenPrimary),
      prefixIconColor: greenPrimary,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide(color: Colors.grey.shade300),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: greenLight, width: 2),
      ),
      filled: true,
      fillColor: greenSoftFill,                          // ✅ color directo
    ),

    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(double.infinity, 50),
        backgroundColor: greenPrimary,
        foregroundColor: white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(40),
        ),
        elevation: 2,
        textStyle: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.bold,
        ),
      ),
    ),

    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: greenPrimary,
      ),
    ),

    cardTheme: CardThemeData(
      elevation: 8,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(24),
      ),
      color: white,
    ),

    textTheme: const TextTheme(
      headlineMedium: TextStyle(
        fontWeight: FontWeight.bold,
        color: greenPrimary,
        fontSize: 26,
      ),
      bodyMedium: TextStyle(
        color: textDark,
      ),
    ),
  );
}