
var qItem = '{{each data}}<div class="quoteItem"><div class="date quotePart">${date} - ${source}</div><div class="quote quotePart">${quote}</div><div class="quotePart">said <span class="who">${who}</span></div><div class="entity quotePart"><p>tags: ${tags}</div></div>{{/each}}';

$.template( "quoteItemTmpl", qItem );