    const digits = document.querySelectorAll('.digit');
    setTimeout(() => {
      digits.forEach((d, i) => {
        const target = d.textContent;
        let count = 0;
        const interval = setInterval(() => {
          d.textContent = Math.floor(Math.random() * 10);
          if (++count > 10) { d.textContent = target; clearInterval(interval); }
        }, 50 + i * 30);
      });
    }, 800);
