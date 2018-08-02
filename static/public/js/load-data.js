function loadData(){
	//加载数据
$.getJSON('/ajax' + location.pathname, function(data){
	if( ! data.error_code ){
		var data_array = data.data;
		// console.log(data_array);
		
		// $('#editable-sample tbody')
		// user data
		if(  location.pathname.search('user') != -1 ){
			for( var i=0; i < data_array.length; i++ ){
				// console.log(i)
				var inner_html = '<tr><td>' + data_array[i].id + '</td> <td>' +data_array[i].username + '</td><td>' + data_array[i].nickname  +'</td> ' +
									'<td><a class="data-edit" href="'+  '/modify'  + location.pathname +  '?uuid='+ data_array[i].uuid + '">编辑</a></td><td><a class="data-delete" data-value="' + data_array[i].uuid +'" href="javascript:;">删除</a></td></tr>';
				// console.log(inner_html);
				$('#editable-sample tbody').append(inner_html);

			};

		}else if( location.pathname.search('question') != -1 ){
			//只显示一半数据
			for( var i=0; i < data_array.length/2; i++ ){
				var inner_html = '<tr><td>' + data_array[i].id + '</td> <td>' +data_array[i].question + '</td><td>' + data_array[i].answer  +'</td> ' +
									'<td>' + data_array[i].explains + '</td>' +
									' <td>' +data_array[i].a + '</td><td>' + data_array[i].b  +'</td> ' + 
									' <td>' +data_array[i].c + '</td><td>' + data_array[i].d  +'</td> ' +
									'<td><img src="' +data_array[i].img + '" alt="题目图片" width="140px" height="100px"></td> ' + 
									'<td><a class="data-edit" href="'+  '/modify'  + location.pathname +  '?uuid='+ data_array[i].uuid + '">编辑</a></td><td><a class="data-delete" data-value="' + data_array[i].uuid + '" href="javascript:;">删除</a></td></tr>';
				$('#editable-sample tbody').append(inner_html);
			}
		};
		
		
	};

	//分页
	$('#editable-sample').DataTable({
			aLengthMenu: [
                    [5, 15, 20, -1],
                    [5, 15, 20, "All"] // change per page values here
                ],
                // set the initial value
                iDisplayLength: 5,
                sDom: "<'row'<'col-lg-6'l><'col-lg-6'f>r>t<'row'<'col-lg-6'i><'col-lg-6'p>>",

                oLanguage: {
                    sLengthMenu: "_MENU_ 每页显示",
                    oPaginate: {
                        sPrevious: "上一页",
                        sNext: "下一页"
                    }
                },
                aoColumnDefs: [{
                        'bSortable': false,
                        'aTargets': [0]
                    }
                ]
		});


});
}

loadData();

