import { serialize } from 'cookie';
import { redirect } from '@sveltejs/kit';

const defaultCookieOpts = {
    httpOnly: false,
    maxAge: 3600 * 1000 * 24 * 365,
    path: '/'
};

export async function POST({ request, cookies }) {
    console.log('reeee');
    const nickname = (await request.formData()).get('nickname') as string;
    cookies.set('nickname', nickname, defaultCookieOpts);
    throw redirect(302, '/');
}
