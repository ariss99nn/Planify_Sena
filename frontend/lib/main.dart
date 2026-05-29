import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/theme/theme.dart';

import 'features/auth/providers/auth_provider.dart';
import 'features/users/providers/user_provider.dart';
import 'features/aulas/providers/aula_provider.dart';

import 'features/auth/guards/auth_guard.dart';

import 'features/auth/screens/login_screen.dart';
import 'features/auth/screens/register_screen.dart';
import 'features/auth/screens/profile_screen.dart';
import 'features/auth/screens/forgot_password_screen.dart';
import 'features/auth/screens/verify_email_screen.dart';
import 'features/auth/screens/reset_password_screen.dart';

import 'features/home/screens/home_screen.dart';
import 'features/users/screens/user_list_screen.dart';
import 'features/aulas/screens/aula_list_screen.dart';
import 'features/aulas/screens/aula_detail_screen.dart';
import 'features/aulas/screens/aula_form_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthProvider()..checkAuth(),
        ),
        ChangeNotifierProvider(
          create: (_) => UserProvider(),
        ),
        ChangeNotifierProvider(
          create: (_) => AulaProvider(),
        ),
      ],
      child: MaterialApp(
        title: 'PLANIFY',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light,
        home: AuthGuard(child: const HomeScreen()),

        // ✅ onGenerateRoute — maneja URLs con segmentos dinámicos (deep links)
        onGenerateRoute: (settings) {
          final uri = Uri.parse(settings.name ?? '');
          final segments = uri.pathSegments;

          // /reset-password/TOKEN — viene del email
          if (segments.first == 'reset-password') {
            return MaterialPageRoute(
              builder: (_) => ResetPasswordScreen(),
              settings: RouteSettings(
                name: '/reset-password',
                arguments: segments.last,
              ),
            );
          }

          // /aulas/123 — detalle por id
          if (segments.length == 2 && segments.first == 'aulas') {
            final id = int.tryParse(segments.last);
            if (id != null) {
              return MaterialPageRoute(
                builder: (_) => AulaDetailScreen(aulaId: id),
                settings: settings,
              );
            }
          }

          return null;
        },

        routes: {
          '/login':          (_) => const LoginScreen(),
          '/register':       (_) => const RegisterScreen(),
          '/profile':        (_) => const ProfileScreen(),
          '/home':           (_) => AuthGuard(child: const HomeScreen()),
          '/users':          (_) => AuthGuard(child: const UserListScreen()),
          '/reset-password': (_) => ResetPasswordScreen(),
          '/verify-email': (ctx) => VerifyEmailScreen(
                email: ModalRoute.of(ctx)!.settings.arguments as String? ?? '',
              ),
          '/aulas':          (_) => AuthGuard(child: const AulaListScreen()),
          '/aulas/nueva':    (_) => AuthGuard(child: const AulaFormScreen()),
        },
      ),
    );
  }
}