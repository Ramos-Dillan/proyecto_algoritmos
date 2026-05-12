import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const roleGuard: CanActivateFn = (route) => {

  const router = inject(Router);

  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const allowedRoles = route.data?.['roles'];

  if (!user.role) {
    return router.createUrlTree(['/login']);
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return router.createUrlTree(['/home']);
  }

  return true;
};