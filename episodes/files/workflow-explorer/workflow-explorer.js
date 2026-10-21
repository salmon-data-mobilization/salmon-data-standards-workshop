    // Chapter 1's progressive comparison. Works offline on the lesson and
    // standalone review page; no model, account or host API is involved.
    (() => {
      const root = document.getElementById('salmon-workflow-guided');
      if (!root) return;
      root.replaceChildren();
      root.append(el('h3', 'workflow-heading', 'Less detective work. More time for the biology.'));
      const controls = el('div', 'tour-controls');
      controls.setAttribute('role', 'group');
      controls.setAttribute('aria-label', 'Workflow timeline controls');
      [['back', 'Previous'], ['next', 'Next'], ['play', 'Play'], ['full', 'Full diagram']].forEach(([id, label]) => {
        const button = el('button', 'btn btn-sm ' + (id === 'next' ? 'btn-primary' : 'btn-outline-secondary'), label);
        button.id = 'salmon-tour-' + id;
        button.type = 'button';
        if (id === 'full' || id === 'play') button.setAttribute('aria-pressed', 'false');
        controls.append(button);
      });
      root.append(controls);
      const progress = el('div', 'tour-position');
      progress.id = 'salmon-tour-position';
      progress.setAttribute('aria-live', 'polite');
      root.append(progress);
      const figure = el('figure');
      figure.setAttribute('aria-label', 'Two routes from the same CU-year question to reusable data');
      const board = el('div', 'canvas');
      board.id = 'salmon-tour-canvas';
      const lines = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      lines.classList.add('lines');
      lines.setAttribute('aria-hidden', 'true');
      board.append(lines, el('div', 'question', 'Assemble annual spawner-abundance estimates for each Conservation Unit (CU), a salmon population grouping, and year.'));
      const laneHeadings = el('div', 'lane-headings');
      [['The usual route', 'Files and scattered explanations'], ['With reviewed Salmon Data Packages', 'The same Yukon and Fraser data, with descriptions included']].forEach(([title, note]) => {
        const heading = el('div', 'lane-heading', title);
        heading.append(el('span', 'text-small', note));
        laneHeadings.append(heading);
      });
      board.append(laneHeadings);
      const stageContainer = el('div');
      stageContainer.id = 'salmon-tour-stages';
      board.append(stageContainer);
      figure.append(board);
      const evidenceCaption = el('figcaption', 'text-small');
      evidenceCaption.id = 'salmon-tour-caption';
      figure.append(evidenceCaption);
      root.append(figure);
      const evidenceLinks = el('div', 'source-links text-small');
      evidenceLinks.id = 'salmon-tour-sources';
      const siteRoot = root.dataset.siteRoot || '';
      [['Yukon excerpt', 'files/intro-comparison/yukon-excerpt.csv'], ['Fraser excerpt', 'files/intro-comparison/fraser-excerpt.csv'], ['Read the source comparison', 'session-1.html#the-archetypical-data-problem']].forEach(([label, href]) => {
        const link = el('a', '', label);
        link.href = siteRoot + href;
        evidenceLinks.append(link);
      });
      root.append(evidenceLinks);
      const announcement = el('div', 'visually-hidden');
      announcement.id = 'salmon-tour-status';
      announcement.setAttribute('aria-live', 'polite');
      root.append(announcement);
      const canvas = root.querySelector('#salmon-tour-canvas');
      const stageRoot = root.querySelector('#salmon-tour-stages');
      const svg = root.querySelector('.lines');
      const back = root.querySelector('#salmon-tour-back');
      const next = root.querySelector('#salmon-tour-next');
      const play = root.querySelector('#salmon-tour-play');
      const full = root.querySelector('#salmon-tour-full');
      const position = root.querySelector('#salmon-tour-position');
      const status = root.querySelector('#salmon-tour-status');
      const sources = root.querySelector('#salmon-tour-sources');
      const caption = root.querySelector('#salmon-tour-caption');
      const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
      const NS = 'http://www.w3.org/2000/svg';
      const part = (label, note = '') => ({label, note});
      const node = (id, label, note, detail, verdict = null) => ({id, label, note, detail, verdict});

      const stages = [
        {
          title: 'Find and understand the data',
          left: [
            node('collect', 'Find the Yukon and Fraser files', 'Yukon mean; Fraser SpnForAbd_Total. Which values answer our question?', [
              part('Yukon Chinook reconstruction', 'A model combines passage, genetic and harvest information to estimate abundance'),
              part('Fraser Rapid Status Assessment', 'An assessment of conservation status with abundance fields among its outputs')
            ]),
            node('documents', 'Find the explanations for each column', 'Read the source dictionaries and methods.', [
              part('Read a data dictionary', 'It explains each column’s meaning, units and possible values'),
              part('Match methods to fields', 'Which fish, places, years and uncertainties do these estimates cover?')
            ]),
            node('provider', 'Ask, wait and ask again', 'Missing explanations can leave an assumption unresolved.', [
              part('Ask the provider about a gap', 'A contact may have moved or retired'),
              part('Clarify the source’s meaning'),
              part('Return to the methods', 'A partial answer can raise another question')
            ])
          ],
          right: [
            node('packages', 'Open the same sources as reviewed packages', 'A Salmon Data Package keeps data and descriptions in a common file structure.', [
              part('Keep original fields and values', 'Yukon mean and Fraser SpnForAbd_Total remain traceable to their sources'),
              part('Read the included data dictionary', 'Column meanings, units and possible values travel with the table'),
              part('Follow methods and source links', 'These descriptions are metadata: information needed to interpret and reuse data'),
              part('Starting with raw files?', 'Draw the relationships, write the dictionary, and review it with a provider or peer')
            ])
          ]
        },
        {
          title: 'Check and combine the estimates',
          left: [
            node('reshape', 'Work out each table’s structure', 'Different column names, population identifiers and year fields.', [
              part('Locate mean and SpnForAbd_Total'),
              part('Identify the population and year', 'Yukon stock/year; Fraser CU_ID/Year'),
              part('Record changes to format', 'Preserve the source values and the link back to each record')
            ]),
            node('join-manual', 'Combine, then revisit the meanings', 'Do both fields describe the abundance we need?', [
              part('Check the included fish and places'),
              part('Check methods and uncertainty'),
              part('Return to the source for gaps', 'The two records concern different Conservation Units; retain both identities')
            ])
          ],
          right: [
            node('join-reviewed', 'Find shared meanings, then review fit', 'mean and SpnForAbd_Total → a shared abundance definition, with their differences retained.', [
              part('Find candidate fields by the shared identifier', 'Different column names can refer to the same characteristic'),
              part('Review fit for the research question', 'A person checks population, year, included fish, methods and uncertainty'),
              part('Combine with explicit mappings', 'Study code uses recorded connections between source fields and meanings')
            ])
          ]
        },
        {
          title: 'Keep the estimates and their limits visible',
          left: [
            node('claim-risk', 'Carry an unchecked interpretation into analysis', 'For example: reading “High confidence” as precise abundance.', [
              part('Fraser 2023: ConfidenceRating = High', 'The same record reports SpnForAbd_Total = 146371'),
              part('Assume it describes abundance precision'),
              part('Make an unsupported precision claim', 'The source definition actually concerns assessment status')
            ], {tone:'caution', label:'Potentially wrong assumption', note:'A plausible label can lead to an unsupported conclusion.'})
          ],
          right: [
            node('claim-checked', 'Keep the evidence with each estimate', 'Retain each CU, year, included fish, method and uncertainty.', [
              part('Keep Yukon and Fraser identities distinct', 'The goal is a set of annual CU estimates with their differences documented'),
              part('Check the Fraser confidence definition', 'ConfidenceRating describes assessment status; it does not establish abundance precision'),
              part('Keep Yukon uncertainty separate', 'lower and upper concern the reconstruction estimate; their exact meaning comes from the methods')
            ], {tone:'checked', label:'Interpretation checked against evidence', note:'The confidence mistake is caught; remaining questions stay visible.'})
          ]
        },
        {
          title: 'Publish once, help the next project',
          left: [
            node('rebuild', 'Reconstruct descriptions at the end', 'The paper is ready; the data publication still needs work.', [
              part('Find the source and processing history'),
              part('Choose a metadata structure', 'A consistent way to record descriptions of the data'),
              part('Recover earlier decisions', 'Important answers may still be in old emails')
            ]),
            node('publish-late', 'Prepare and publish the data', 'Incomplete explanations leave work for the next team.', [
              part('Review rights, credit and descriptions'),
              part('Deposit and release the dataset'),
              part('Answer the next user’s questions', 'The clarification work may be repeated')
            ])
          ],
          right: [
            node('publish-ready', 'Validate, publish and pass on the explanations', 'Source packages and the combined dataset preserve the work.', [
              part('Build and check packages with metasalmon', 'This R software helps create, review and validate package files'),
              part('Credit providers and package authors', 'Review rights and preserve the source and processing history'),
              part('Prepare the catalog description and upload', 'KNB, the Knowledge Network for Biocomplexity, is a research-data catalog'),
              part('Release through the catalog', 'Publication and a persistent citation identifier are separate from upload'),
              part('Reuse packages and shared definitions', 'Later users can start with these reviewed explanations')
            ])
          ],
          result: ['Next team: repeat the detective work', 'Next team: reuse the records and their meanings']
        }
      ];

      let stageIndex = 0;
      let showFull = false;
      let expanded = new Set();
      let playing = false;
      let timer = 0;
      let frame = 0;
      let animateNext = false;

      function el(tag, className, text) {
        const item = document.createElement(tag);
        if (className) item.className = className;
        if (text) item.textContent = text;
        return item;
      }

      function stopPlayback() {
        playing = false;
        clearTimeout(timer);
        play.textContent = stageIndex === 3 && !showFull ? 'Replay' : 'Play';
        play.setAttribute('aria-pressed', 'false');
      }

      function scheduleAdvance() {
        clearTimeout(timer);
        if (!playing) return;
        timer = window.setTimeout(() => {
          if (stageIndex === 3) {
            stopPlayback();
            return;
          }
          stageIndex += 1;
          render(true);
          scheduleAdvance();
        }, 7000);
      }

      function buildMeaningExample() {
        const example = el('div', 'meaning-example');
        example.append(el('h5', '', 'Two records, one shared characteristic'));
        example.append(el('p', 'text-small', 'Teaching draft: proposed descriptions for review.'));
        const records = el('div', 'meaning-records');
        [
          ['Yukon mean', '2009.4529003227', 'NorthernYukonR.andtribs. · 2023', 'Retain the reconstruction method and uncertainty; confirm the CU identifier and included fish.'],
          ['Fraser SpnForAbd_Total', '146371', 'CK-03 · 2023', 'Retain total versus wild scope, estimation method and status confidence separately.']
        ].forEach(([field, value, context, note]) => {
          const record = el('div', 'meaning-record text-small');
          record.append(el('strong', '', field), el('div', '', value), el('div', '', context), el('p', '', note));
          records.append(record);
        });
        example.append(records);
        const shared = el('p', 'shared-meaning');
        shared.append(document.createTextNode('Both descriptions → property: '));
        const term = el('a', '', 'Abundance');
        term.href = 'https://github.com/salmon-data-mobilization/salmon-domain-ontology/blob/d45f8f7cc857d92af8bbe54a7c89b2a4a14784b2/ontology/modules/02-observation-measurement.ttl#L27-L33';
        shared.append(term);
        example.append(shared);
        example.append(el('p', 'text-small', 'A property is the characteristic represented by an estimate. Each record keeps its own population, year, method and other context.'));
        example.append(el('p', 'text-small', 'A controlled vocabulary supplies maintained terms and definitions. An ontology models concepts and their relationships in a form software can interpret. The Salmon Domain Ontology supplies this abundance term.'));
        const identifier = el('p', 'text-small');
        identifier.append(document.createTextNode('Its Internationalized Resource Identifier (IRI), a stable name for the concept, is '), el('code', '', 'https://w3id.org/smn/Abundance'), document.createTextNode('.'));
        example.append(identifier);
        return example;
      }

      function buildNode(item, laneNumber) {
        const open = expanded.has(item.id);
        const container = el('div', 'node');
        container.dataset.node = item.id;
        container.dataset.lane = laneNumber;
        if (open) container.dataset.expanded = 'true';
        const label = item.label + (open ? ' −' : ' +');
        const button = el('button', 'btn btn-sm btn-outline-secondary', label);
        button.type = 'button';
        button.dataset.label = label;
        button.setAttribute('aria-label', label);
        button.setAttribute('aria-expanded', String(open));
        button.setAttribute('aria-controls', 'guided-detail-' + item.id);
        button.addEventListener('click', () => {
          stopPlayback();
          if (expanded.has(item.id)) expanded.delete(item.id); else expanded.add(item.id);
          render(true);
          stageRoot.querySelector('[data-node="' + item.id + '"] button').focus({preventScroll:true});
          status.textContent = item.label + ': ' + (expanded.has(item.id) ? 'detail opened within the diagram' : 'detail closed');
        });
        container.append(button, el('div', 'node-caption text-small', item.note));
        if (item.verdict) {
          const verdict = el('div', 'verdict');
          verdict.dataset.tone = item.verdict.tone;
          const symbol = el('span', 'symbol');
          symbol.textContent = item.verdict.tone === 'checked' ? '✓' : '⚠';
          symbol.setAttribute('aria-hidden', 'true');
          verdict.append(symbol, el('div', 'verdict-label', item.verdict.label), el('div', 'text-small', item.verdict.note));
          container.append(verdict);
        }
        const nested = el('div', 'nested');
        nested.id = 'guided-detail-' + item.id;
        nested.hidden = !open;
        if (item.id === 'join-reviewed') nested.append(buildMeaningExample());
        item.detail.forEach(detail => {
          const itemNode = el('div', 'nested-node');
          itemNode.append(el('strong', '', detail.label));
          if (detail.note) itemNode.append(el('span', 'text-small', detail.note));
          nested.append(itemNode);
        });
        container.append(nested);
        return container;
      }

      function render(animate = false) {
        back.disabled = showFull || stageIndex === 0;
        next.disabled = showFull || stageIndex === 3;
        full.setAttribute('aria-pressed', String(showFull));
        full.textContent = showFull ? 'Return to tour' : 'Full diagram';
        play.textContent = playing ? 'Pause' : stageIndex === 3 && !showFull ? 'Replay' : 'Play';
        play.setAttribute('aria-pressed', String(playing));
        position.textContent = showFull ? 'Whole project · fewer repeated preparation tasks' : (stageIndex + 1) + ' of 4 · ' + stages[stageIndex].title;
        stageRoot.replaceChildren();
        const visibleStages = showFull ? stages : stages.slice(0, stageIndex + 1);
        visibleStages.forEach(stage => {
          const section = el('div', 'stage');
          section.dataset.stage = stages.indexOf(stage);
          const stageHeader = el('div', 'stage-header');
          const stageHeading = el('div', 'stage-heading');
          stageHeading.append(el('span', 'phase-number', 'Phase ' + (stages.indexOf(stage) + 1)), el('h4', 'stage-title', stage.title));
          stageHeader.append(el('hr'), stageHeading, el('hr'));
          section.append(stageHeader);
          const columns = el('div', 'stage-columns');
          [stage.left, stage.right].forEach((items, laneNumber) => {
            const lane = el('div', 'lane');
            lane.dataset.lane = laneNumber;
            items.forEach(item => lane.append(buildNode(item, laneNumber)));
            if (stage.result) lane.append(el('div', 'reuse-result text-small', stage.result[laneNumber]));
            columns.append(lane);
          });
          section.append(columns);
          stageRoot.append(section);
        });
        const showEvidence = showFull || stageIndex >= 1;
        sources.hidden = !showEvidence;
        caption.hidden = !showEvidence;
        caption.textContent = showEvidence
          ? 'The proposed package descriptions need review. A shared abundance term helps find candidate fields; it does not resolve every difference. Spacing does not measure time.'
          : '';
        if (showFull || stageIndex >= 2) caption.textContent += ' The confidence mistake is an invented misreading of real fields, not an error attributed to the source authors.';
        if (showFull || stageIndex === 3) caption.textContent += ' Workshop publication uses a test catalog; the expanded release steps describe a later production route.';
        animateNext = animate && !motion.matches;
        requestDraw();
      }

      function svgEl(tag, attributes) {
        const item = document.createElementNS(NS, tag);
        Object.entries(attributes || {}).forEach(([key,value]) => item.setAttribute(key, String(value)));
        return item;
      }

      function rectOf(item, origin) {
        const b = item.getBoundingClientRect();
        return {x:b.left-origin.left,y:b.top-origin.top,w:b.width,h:b.height,cx:b.left-origin.left+b.width/2,bottom:b.bottom-origin.top};
      }

      function connect(d, type) {
        const edge = svgEl('path', {d,class:type+'-line','marker-end':'url(#guided-arrow-'+type+')'});
        svg.append(edge);
        return edge;
      }

      function wrapLabels() {
        const limit = Math.max(9, Math.min(33, Math.floor(((canvas.clientWidth - 70) / 2 - 46) / 7.5)));
        stageRoot.querySelectorAll('button').forEach(button => {
          if (button.dataset.wrap === String(limit)) return;
          button.dataset.wrap = String(limit);
          const label = el('span');
          let line = '';
          button.dataset.label.replace(/ ([+−])$/, '\u00a0$1').split(' ').forEach(word => {
            if (line && (line+' '+word).length > limit) {
              label.append(document.createTextNode(line), document.createElement('br'));
              line = word;
            } else line += (line ? ' ' : '') + word;
          });
          label.append(document.createTextNode(line));
          button.replaceChildren(label);
        });
      }

      function draw() {
        wrapLabels();
        const origin = canvas.getBoundingClientRect();
        const previousEdges = new Set([...svg.querySelectorAll('path[class$="-line"]')].map(edge => edge.getAttribute('class') + ':' + edge.getAttribute('d')));
        svg.setAttribute('width', origin.width);
        svg.setAttribute('height', origin.height);
        svg.setAttribute('viewBox', '0 0 '+origin.width+' '+origin.height);
        svg.replaceChildren();
        const defs = svgEl('defs');
        [['usual','var(--muted-foreground)'],['package','var(--viz-series-1)'],['loop','var(--orange)']].forEach(([name,color]) => {
          const arrow = svgEl('marker',{id:'guided-arrow-'+name,viewBox:'0 0 8 8',refX:7,refY:4,markerWidth:6,markerHeight:6,orient:'auto'});
          arrow.append(svgEl('path',{d:'M 1 1 L 7 4 L 1 7',fill:'none',stroke:color,'stroke-width':1.5}));
          defs.append(arrow);
        });
        svg.append(defs);
        const question = rectOf(root.querySelector('.question'), origin);
        const headings = [...root.querySelectorAll('.lane-heading')].map(item => rectOf(item, origin));
        const lanes = [0,1].map(n => [...stageRoot.querySelectorAll('.node[data-lane="'+n+'"]')]);
        const phaseBands = [...stageRoot.querySelectorAll('.stage-header')].map(item => rectOf(item, origin));

        // Leave a clear band around each phase heading as the timeline extends.
        function connectTimeline(x, start, end, type) {
          let cursor = start;
          const segments = [];
          phaseBands.forEach(band => {
            if (band.bottom + 6 <= cursor || band.y - 6 >= end) return;
            if (band.y - 6 > cursor) segments.push('M ' + x + ' ' + cursor + ' V ' + (band.y - 6));
            cursor = Math.min(end, band.bottom + 6);
          });
          if (cursor < end) segments.push('M ' + x + ' ' + cursor + ' V ' + end);
          if (segments.length) connect(segments.join(' '), type);
        }

        lanes.forEach((nodes, laneNumber) => {
          const type = laneNumber ? 'package' : 'usual';
          const heading = headings[laneNumber];
          const first = rectOf(nodes[0],origin);
          connect('M '+question.cx+' '+question.bottom+' V '+(question.bottom+11)+' H '+heading.cx+' V '+(heading.y-5),type);
          connectTimeline(heading.cx, heading.bottom + 5, first.y - 5, type);
          nodes.forEach((item,index) => {
            const b = rectOf(item,origin);
            if (item.dataset.expanded) {
              svg.append(svgEl('rect',{x:b.x,y:b.y,width:b.w,height:b.h,rx:8,class:'group-box'}));
              const parts = [...item.querySelectorAll('.nested-node')].map(n => rectOf(n,origin));
              parts.forEach(p => svg.append(svgEl('rect',{x:p.x,y:p.y,width:p.w,height:p.h,rx:6,class:'detail-box'})));
              for (let i=0;i<parts.length-1;i++) connect('M '+parts[i].cx+' '+(parts[i].bottom+2)+' V '+(parts[i+1].y-4),type);
            }
            if (index < nodes.length-1) {
              const destination = rectOf(nodes[index+1],origin);
              connectTimeline(b.cx, b.bottom + 2, destination.y - 5, type);
            }
          });
        });

        function anchor(id) {
          const item = stageRoot.querySelector('[data-node="'+id+'"]');
          if (!item) return null;
          return rectOf(item.dataset.expanded ? item : item.querySelector('button'),origin);
        }
        function loop(from,to) {
          const a = anchor(from), b = anchor(to);
          if (!a || !b) return;
          const outer = Math.max(2,Math.min(a.x,b.x)-15);
          connect('M '+(a.x-2)+' '+(a.y+Math.min(a.h/2,22))+' H '+outer+' V '+(b.y+Math.min(b.h/2,22))+' H '+(b.x-3),'loop');
        }
        loop('provider','documents');
        loop('join-manual','documents');

        if (animateNext && !motion.matches) {
          svg.querySelectorAll('path[class$="-line"]').forEach(edge => {
            if (previousEdges.has(edge.getAttribute('class') + ':' + edge.getAttribute('d'))) return;
            const length = edge.getTotalLength();
            if (length > 0) edge.animate([{strokeDasharray:length,strokeDashoffset:length},{strokeDasharray:length,strokeDashoffset:0}],{duration:650,easing:'ease-out'});
          });
        }
        animateNext = false;
      }

      function requestDraw() {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(draw);
      }
      back.addEventListener('click', () => {
        stopPlayback(); stageIndex = Math.max(0,stageIndex-1); render(true);
      });
      next.addEventListener('click', () => {
        stopPlayback(); stageIndex = Math.min(3,stageIndex+1); render(true);
      });
      full.addEventListener('click', () => {
        stopPlayback(); showFull = !showFull; render(true);
      });
      play.addEventListener('click', () => {
        if (playing) {stopPlayback(); return;}
        if (showFull || stageIndex === 3) stageIndex = 0;
        showFull = false;
        expanded.clear();
        playing = true;
        render(true); scheduleAdvance();
      });
      document.addEventListener('visibilitychange', () => {if (document.hidden) stopPlayback();});
      new ResizeObserver(requestDraw).observe(canvas);
      render();
    })();
