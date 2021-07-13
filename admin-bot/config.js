const sleep = time => new Promise(resolve => setTimeout(resolve, time))

const challenges = new Map([
  ['pastebin-1', {
    name: 'Pastebin 1',
    timeout: 7000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'flag',
        value: 'flag{d1dn7_n33d_70_b3_1n_ru57}',
        url: 'https://pastebin-1.mc.ax',
        secure: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(3000)
    },
  }],
  ['pastebin-2-social-edition', {
    name: 'Pastebin 2 Social Edition',
    timeout: 10000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'flag',
        value: 'flag{m4yb3_ju57_a_l177l3_5u5p1c10u5}',
        url: 'https://pastebin-2-social-edition.mc.ax',
        secure: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(3000)
      try {
        await page.evaluate(() => {
          document.querySelector('input[name=author]').value = 'admin'
          document.querySelector('textarea[name=content]').innerText = 'Nice paste!'
          document.querySelector('input[type=submit]').click()
        })
      } catch {}
      await sleep(3000)
    },
  }],
  ['pastebin-3', {
    name: 'Pastebin 3',
    timeout: 65000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'session',
        value: 'eyJ1c2VybmFtZSI6ImFkbWluIn0.YOT4QA._oyXzLh4yCqVwW5PczYmH07XTww',
        url: 'https://pastebin-3.mc.ax',
        secure: true,
        httpOnly: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(60000)
    },
  }],
  ['notes', {
    name: 'Notes',
    timeout: 7000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'username',
        value: 'admin.uPoq5EHI5BXHy3ifvT25%2Fds2M3JH2JwsZJPpN0Vn1s8',
        url: 'https://notes.mc.ax',
        secure: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(3000)
    },
  }],
  ['mdbin', {
    name: 'MdBin',
    timeout: 7000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'flag',
        value: 'flag{d1d_y0u_kn0w_unified_cr4sh3s_1mm3di4t3ly_0n_p0llut10n?}',
        url: 'https://mdbin.mc.ax',
        secure: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(3000)
    },
  }],
  ['wtjs', {
    name: 'WTJS',
    timeout: 5000,
    handler: async (url, ctx) => {
      const page = await ctx.newPage()
      await page.setCookie({
        name: 'flag',
        value: 'flag{n0t_qu1t3_jsf*ck_but_cl0s3_3n0ugh}',
        url: 'https://wtjs.mc.ax',
        secure: true,
      })
      await page.goto(url, { timeout: 3000, waitUntil: 'domcontentloaded' })
      await sleep(3000)
    },
  }],
])

module.exports = {
  challenges,
}
