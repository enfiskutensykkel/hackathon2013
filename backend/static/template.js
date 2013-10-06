
var qItem = '{{each data}}<div class="quoteItem"><div class="date quotePart"><a href="${url}">${date} - ${source} - ${headline}</a></div><div class="quote quotePart">"${quote}", </div><div class="quotePart">said <span class="who">${who}</span></div><div class="tagList quotePart">{{each tags}}<span class="tag ${$value}">${$value}</span>{{/each}}</div></div>{{/each}}';

$.template( "quoteItemTmpl", qItem );