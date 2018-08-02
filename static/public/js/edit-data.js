//加载数据
// $.getJSON('/ajax' + location.pathname, function(data){
// 	if( ! data.error_code ){
// 		var data_array = data.data;
// 		// console.log(data_array);
		
// 		// $('#editable-sample tbody')
// 		// user data
// 		if(  location.pathname.search('user') != -1 ){
// 			for( var i=0; i < data_array.length; i++ ){
// 				// console.log(i)
// 				var inner_html = '<tr><td>' + data_array[i].id + '</td> <td>' +data_array[i].username + '</td><td>' + data_array[i].nickname  +'</td> ' +
// 									'<td><a class="data-edit" href="javascript:;">编辑</a></td><td><a class="data-delete" data-value="' + data_array[i].uuid +'" href="javascript:;">删除</a></td></tr>';
// 				// console.log(inner_html);
// 				$('#editable-sample tbody').append(inner_html);

// 			};

// 		}else if( location.pathname.search('question') != -1 ){
// 			//只显示
// 			for( var i=0; i < data_array.length/2; i++ ){
// 				var inner_html = '<tr><td>' + data_array[i].id + '</td> <td>' +data_array[i].question + '</td><td>' + data_array[i].answer  +'</td> ' +
// 									'<td>' + data_array[i].explains + '</td>' +
// 									' <td>' +data_array[i].a + '</td><td>' + data_array[i].b  +'</td> ' + 
// 									' <td>' +data_array[i].c + '</td><td>' + data_array[i].d  +'</td> ' +
// 									'<td><img src="' +data_array[i].img + '" alt="题目图片" width="140px" height="100px"></td> ' + 
// 									'<td><a class="data-edit" href="'+  '/modify'  + location.pathname +  '?uuid='+ data_array[i].uuid + '">编辑</a></td><td><a class="data-delete" data-value="' + data_array[i].uuid + '" href="javascript:;">删除</a></td></tr>';
// 				$('#editable-sample tbody').append(inner_html);
// 			}
// 		};
		
		
// 	}
// });




//添加按钮
$('.add-data-btn').on('click', function(){
	var href_str = "/modify" + location.pathname;
	$(this).attr('href', href_str);
})




//修改数据
$('.data-edit').on('click', function(){
	var uuid = $(this).attr("data-value");
	var href_str = "/modify" + location.pathname + '?uuid=' + uuid;
	// console.log(href_str);
	$(this).attr('href', href_str);
})





//删除数据
$(".data-delete").on('click', function(){
	var uuid = $(this).attr("data-value");
	// 待删除元素做标记
	$(this).parent('td').parent('tr').addClass('for-delete-data');
	// alert(uuid);
	console.log(location.pathname)
	$.ajax({
		'type': 'get',
		'url':  '/del' + location.pathname,
		'data':{
			'uuid': uuid,
		},
		'success': function(data){
			if( ! data.error_code ){
				$('.for-delete-data').html('');
				//alert('删除成功!');
				layer.open({
                          title: '提示信息'
                          ,content: '数据删除成功!'
                        });

			}else{
				//alert('删除失败!')
				layer.open({
                          title: '提示信息'
                          ,content: '数据删除失败!'
                        });
			};
		},
	});
});







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





//添加数据
//<tr class="add"> </tr>
// <td class=" sorting_1"><input type="text" class="form-control small" value=""></td>
// <td class=""><input type="text" class="form-control small" value=""></td>
// <td class=""><input type="text" class="form-control small" value=""></td>
// <td class=""><input type="text" class="form-control small" value=""></td>
// <td class=""><a class="edit" href="">Save</a></td>
// <td class=""><a class="cancel" href="">Cancel</a></td>
// </tr>
// $('.add-data-btn').on('click', function(){
// 	// console.log($(this));
// 	var len_addinput = $('#editable-sample > thead > tr').find('th').length -2;
// 	var html_save_btn = '<td class=""><a class="add-data-btn" href="">保存</a></td>';
// 	var html_cancel_btn = '<td class=""><a class="cancel-back-btn" href="">取消</a></td>';
// 	// console.log(len_addinput);
// 	$('#editable-sample > tbody').find('tr').before('<tr class="add-empty-data"> </tr>');


// 		for( var i=0; i< len_addinput; i++ ){
// 		var hmtl_str = '<td class=""><input type="text" class="form-control small" value=""></td>';
// 		$('.add-empty-data').append(hmtl_str);
// 	}
// 	$('.add-empty-data').append(html_save_btn);
// 	$('.add-empty-data').append(html_cancel_btn);
// 	$('.add-empty-data').removeClass('add-empty-data');

	

	
// });


// //取消按钮
// $('.cancel-back-btn').on('click', function(){
// 	console.log($(this))
// 	$(this).parents('tr').remove();
// })

