import { redirect } from '@sveltejs/kit';

export const load = (async ({ cookies }) => {
  const nickname = cookies.get('nickname');
  if (!nickname) {
    throw redirect(302, '/login');
  }

  return { nickname };
});
