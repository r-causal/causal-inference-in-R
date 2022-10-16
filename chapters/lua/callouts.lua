function Div(el)
  if quarto.doc.isFormat("html") then
    callouts = {'callout-tip', 'callout-note', 'callout-warning', 
              'callout-caution', 'callout-important'}
    for key, val in pairs(callouts) do
      if el.classes:includes(val) then
        el.attributes["collapse"] = 'false'
        return el
      end
    end
  end
end 
