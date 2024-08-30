import { test as setup } from '@playwright/test';

setup('prep db', async () => {
    console.log('seeding db')
    require('child_process').exec('npm run db:seed')
})
