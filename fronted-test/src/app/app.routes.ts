import { Routes } from '@angular/router';
import { authGuard } from './features/guards/auth.guards';
import { roleGuard } from './features/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'auth', pathMatch: 'full' },

  {
    path: 'auth',
    loadComponent: () =>
      import('./features/layout/auth-shell/auth-shell')
        .then(m => m.AuthShellComponent)
  },

  { path: 'login', redirectTo: 'auth', pathMatch: 'full' },
  { path: 'register', redirectTo: 'auth', pathMatch: 'full' },

  { path: 'home', loadComponent: () => import('./features/home/home').then(m => m.HomeComponent), canActivate: [authGuard] },
  { path: 'dashboard', loadComponent: () => import('./features/dashboard/dashboard').then(m => m.Dashboard), canActivate: [authGuard] },
  { path: 'therapeutic-groups', loadComponent: () => import('./features/therapeutic-groups/therapeutic-groups').then(m => m.TherapeuticGroupsComponent), canActivate: [authGuard] },
  { path: 'products', loadComponent: () => import('./features/products/products').then(m => m.ProductsComponent), canActivate: [authGuard] },
  { path: 'products/:id', loadComponent: () => import('./features/products/product-detail').then(m => m.ProductDetail), canActivate: [authGuard] },
  { path: 'roles', loadComponent: () => import('./features/roles/roles').then(m => m.RolesComponent), canActivate: [authGuard, roleGuard], data: { roles: ['admin'] } },
  { path: 'forgot-password', loadComponent: () => import('./features/forgot-password/forgot-password').then(m => m.ForgotPassword) },
  { path: 'reset-password', loadComponent: () => import('./features/reset-password/reset-password').then(m => m.ResetPassword) },

  { path: '**', redirectTo: 'auth' }
];